import json
import os


def pytest_terminal_summary(terminalreporter, config):
    """
    测试结束后生成汇总：只统计实际执行的用例（排除 deselected）。
    """
    stats = terminalreporter.stats

    def cnt(key: str) -> int:
        return len(stats.get(key, []))

    # 基本分类
    passed = cnt("passed")
    failed = cnt("failed")
    errors = cnt("error")  # pytest 中的报错（等价于“broken”概念）
    skipped = cnt("skipped")
    xfailed = cnt("xfailed")
    xpassed = cnt("xpassed")
    deselected = cnt("deselected")

    # 仅统计“实际执行”的用例总数（排除被标记过滤掉的 deselected）
    executed_total = passed + failed + errors + skipped + xfailed + xpassed

    # 通过率：含跳过 / 不含跳过
    def pct(n: int, d: int) -> float:
        return round(n / d * 100, 2) if d > 0 else 0.0

    pass_rate_incl_skipped = pct(passed, executed_total)
    pass_rate_excl_skipped = pct(passed, executed_total - skipped)

    summary = {
        # 执行结果
        "executed_total": executed_total,  # 只统计真正执行的总数
        "passed": passed,
        "failed": failed,
        "errors": errors,  # 可与 failed 一起作为失败统计
        "skipped": skipped,
        "xfailed": xfailed,
        "xpassed": xpassed,

        # 被过滤掉的数量（不计入 executed_total）
        "deselected": deselected,

        # 通过率
        "pass_rate_incl_skipped": pass_rate_incl_skipped,
        "pass_rate_excl_skipped": pass_rate_excl_skipped,
    }

    # 写到项目根下的 allure_results 目录
    results_dir = os.path.join(config.rootpath, "allure_results")
    os.makedirs(results_dir, exist_ok=True)
    out_file = os.path.join(results_dir, "pytest_summary.json")

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
