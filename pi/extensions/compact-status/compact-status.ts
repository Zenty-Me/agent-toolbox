import type { Usage } from "@earendil-works/pi-ai";
import type { ExtensionAPI, ExtensionContext, SessionEntry } from "@earendil-works/pi-coding-agent";
import { truncateToWidth, visibleWidth } from "@earendil-works/pi-tui";

function formatTokens(value: number): string {
	if (!Number.isFinite(value)) return "?";
	if (value < 1_000) return String(value);
	const divisor = value < 1_000_000 ? 1_000 : 1_000_000;
	return `${(value / divisor).toFixed(1).replace(/\.0$/, "")}${divisor === 1_000 ? "k" : "M"}`;
}

function elapsed(since: number): string {
	const seconds = Math.max(0, Math.floor((Date.now() - since) / 1_000));
	return seconds < 60 ? `${seconds}s` : `${Math.floor(seconds / 60)}m${String(seconds % 60).padStart(2, "0")}s`;
}

function singleLine(text: string): string {
	return text.replace(/[\r\n\t]/g, " ").replace(/ {2,}/g, " ").trim();
}

function joinSides(left: string, right: string, width: number): string {
	const available = width - visibleWidth(right) - 2;
	if (available < 1) return truncateToWidth(right, width);
	const fitted = truncateToWidth(left, available);
	return fitted + " ".repeat(width - visibleWidth(fitted) - visibleWidth(right)) + right;
}

function usageTotals(entries: SessionEntry[]) {
	const totals = { input: 0, output: 0, cost: 0, cacheHit: undefined as number | undefined };
	for (const entry of entries) {
		let usage: Usage | undefined;
		if (entry.type === "usage" || entry.type === "compaction" || entry.type === "branch_summary") {
			usage = entry.usage;
		} else if (entry.type === "message") {
			const message = entry.message;
			if (message.role === "assistant" || message.role === "toolResult") usage = message.usage;
			if (message.role === "assistant") {
				const prompt = message.usage.input + message.usage.cacheRead + message.usage.cacheWrite;
				totals.cacheHit = prompt > 0 ? message.usage.cacheRead / prompt * 100 : undefined;
			}
		}
		if (!usage) continue;
		totals.input += usage.input;
		totals.output += usage.output;
		totals.cost += usage.cost.total;
	}
	return totals;
}

export default function (pi: ExtensionAPI) {
	let enabled = true;
	let active = false;
	let phase = "就绪";
	let startedAt = 0;
	let compactStartedAt = 0;
	let waitingForUser = false;
	let requestRender: (() => void) | undefined;
	let disposeFooter: (() => void) | undefined;
	const tools = new Map<string, { name: string; since: number }>();

	function setPhase(next: string) {
		if (phase === next) return;
		phase = next;
		requestRender?.();
	}

	function status() {
		if (waitingForUser) return "等待确认";
		if (compactStartedAt) return `压缩中 · ${elapsed(compactStartedAt)}`;
		const tool = tools.values().next().value;
		if (tool) return `执行 ${truncateToWidth(tool.name, 24)}${tools.size > 1 ? ` +${tools.size - 1}` : ""} · ${elapsed(tool.since)}`;
		return active ? `${phase} · ${elapsed(startedAt)}` : phase;
	}

	function install(ctx: ExtensionContext) {
		if (ctx.mode !== "tui") return;
		ctx.ui.setFooter(enabled ? (tui, theme, footerData) => {
			requestRender = () => tui.requestRender();
			const unsubscribe = footerData.onBranchChange(requestRender);
			const timer = setInterval(() => {
				if (active || compactStartedAt || tools.size) tui.requestRender();
			}, 1_000);
			timer.unref();
			let disposed = false;
			let statsKey = "";
			let totals = usageTotals([]);
			const dispose = () => {
				if (disposed) return;
				disposed = true;
				clearInterval(timer);
				unsubscribe();
				requestRender = undefined;
			};
			disposeFooter = dispose;

			return {
				dispose,
				invalidate() {},
				render(width: number): string[] {
					if (width < 1) return [];
					const manager = ctx.sessionManager;
					const key = `${manager.getSessionId()}:${manager.getLeafId()}`;
					if (key !== statsKey) {
						totals = usageTotals(manager.getEntries());
						statsKey = key;
					}

					const model = ctx.model;
					let modelText = theme.fg("accent", singleLine(model?.id ?? "未选择模型"));
					if (model?.reasoning && width >= 45) {
						modelText += theme.fg("muted", ` · 思考 ${ctx.thinkingLevel ?? pi.getThinkingLevel()}`);
					}
					if (model && width >= 110) {
						modelText = theme.fg("dim", `${truncateToWidth(singleLine(model.provider), 20)} · `) + modelText;
					}
					const cwd = manager.getCwd().replace(/\\/g, "/").replace(/\/$/, "");
					const folder = singleLine(cwd.split("/").pop() || cwd || "/");
					const branch = footerData.getGitBranch();
					const location = theme.fg("muted", folder + (branch ? ` · ${singleLine(branch)}` : ""));

					const usage = ctx.getContextUsage();
					const percent = usage?.percent;
					const known = percent != null && Number.isFinite(percent);
					const contextColor = known && percent > 90 ? "error" : known && percent > 70 ? "warning" : "muted";
					const window = usage?.contextWindow ?? model?.contextWindow;
					const percentText = known ? `${percent.toFixed(1).replace(/\.0$/, "")}%` : "?";
					let context = `上下文 ${percentText}`;
					if (window && width >= 80) context += `/${formatTokens(window)}`;
					let stats = theme.fg(contextColor, context);
					const stateColor = waitingForUser ? "warning" : active || compactStartedAt ? "accent" : "success";
					const state = theme.fg(stateColor, singleLine(status()));
					const right = truncateToWidth(state, Math.max(4, width - visibleWidth(stats) - 2));
					const extras = [
						`输入 ${formatTokens(totals.input)} · 输出 ${formatTokens(totals.output)}`,
						...(totals.cacheHit === undefined ? [] : [`缓存 ${totals.cacheHit.toFixed(0)}%`]),
						...(totals.cost > 0 ? [`估费 $${totals.cost.toFixed(3)}`] : []),
						...(pi.getSettings().compaction?.enabled === false ? ["手动压缩"] : []),
					];
					for (const extra of extras) {
						const candidate = stats + theme.fg("dim", ` · ${extra}`);
						if (visibleWidth(candidate) + visibleWidth(right) + 2 <= width) stats = candidate;
					}
					const lines = [joinSides(location, modelText, width), joinSides(stats, right, width)];
					const statuses = [...footerData.getExtensionStatuses()].sort(([a], [b]) => a.localeCompare(b));
					if (statuses.length) {
						const text = statuses.map(([, value]) => singleLine(value)).filter(Boolean).join(" · ");
						if (text) lines.push(truncateToWidth(text, width));
					}
					return lines;
				},
			};
		} : undefined);
	}

	pi.on("session_start", (_event, ctx) => {
		active = !ctx.isIdle();
		startedAt = Date.now();
		phase = active ? "处理中" : "就绪";
		tools.clear();
		compactStartedAt = 0;
		waitingForUser = false;
		install(ctx);
	});
	pi.on("agent_start", () => {
		active = true;
		startedAt = Date.now();
		setPhase("等待响应");
	});
	pi.on("turn_start", () => setPhase("等待响应"));
	pi.on("message_update", (event) => {
		const type = event.assistantMessageEvent.type;
		if (type.startsWith("thinking_")) setPhase("思考中");
		else if (type.startsWith("text_")) setPhase("生成中");
		else if (type.startsWith("toolcall_")) setPhase("准备工具");
	});
	pi.on("message_end", (event) => {
		if (active && event.message.role === "assistant") setPhase("处理中");
	});
	pi.on("tool_execution_start", (event) => {
		tools.set(event.toolCallId, { name: singleLine(event.toolName), since: Date.now() });
		requestRender?.();
	});
	pi.on("tool_execution_end", (event) => {
		tools.delete(event.toolCallId);
		requestRender?.();
	});
	pi.on("agent_settled", (event) => {
		active = false;
		waitingForUser = false;
		tools.clear();
		setPhase(event.aborted ? "已停止" : "就绪");
	});
	pi.on("ui_prompt_start", () => { waitingForUser = true; requestRender?.(); });
	pi.on("ui_prompt_end", () => { waitingForUser = false; requestRender?.(); });
	pi.on("session_before_compact", () => { compactStartedAt = Date.now(); requestRender?.(); });
	const finishCompaction = () => { compactStartedAt = 0; requestRender?.(); };
	pi.on("session_compact", finishCompaction);
	pi.on("session_compact_failed", finishCompaction);
	pi.on("session_shutdown", () => { disposeFooter?.(); disposeFooter = undefined; });

	pi.registerCommand("statusbar", {
		description: "切换精简状态栏：/statusbar [on|off]（关闭即恢复 Pi 默认底栏）",
		handler: async (args, ctx) => {
			if (ctx.mode !== "tui") {
				ctx.ui.notify("状态栏仅在 Pi 终端界面中可用。", "warning");
				return;
			}
			const action = args.trim().toLowerCase();
			if (action && action !== "on" && action !== "off") {
				ctx.ui.notify("用法：/statusbar [on|off]；不带参数切换。", "info");
				return;
			}
			enabled = action ? action === "on" : !enabled;
			install(ctx);
			ctx.ui.notify(enabled ? "已启用精简状态栏。" : "已恢复 Pi 默认状态栏。", "info");
		},
	});
}
