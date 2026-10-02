#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calc_verify.py — 资料分析精确计算验证器
用途：秒杀答案的机器验证兜底（保正确率），边界值题型必须精确计算。
公式输入用小数（5.3% → 0.053）。

用法示例：
  python calc_verify.py --mode base --cur 5631.6 --rate 0.078        # 基期量=现期/(1+r)
  python calc_verify.py --mode growth-amt --cur 1057 --rate 0.053   # 增长量(现期,r)
  python calc_verify.py --mode growth-amt2 --base 1000 --rate 0.053 # 增长量(基期,r)
  python calc_verify.py --mode rate --base 1000 --cur 1053          # 增长率
  python calc_verify.py --mode rate2 --delta 53 --cur 1053           # 增长率(增量,现期)
  python calc_verify.py --mode interval --r1 0.15 --r2 0.08         # 间隔增长率
  python calc_verify.py --mode mix --a 4.6 --wa 454.70 --b 3.6 --wb 847.97  # 混合增长率(%,万人)
  python calc_verify.py --mode avg --cur 100 --base 80 --years 3    # 年均增长率
  python calc_verify.py --mode avg-amt --cur 100 --base 80 --years 3  # 年均增长量
  python calc_verify.py --mode proportion --part 609.0 --whole 2582.0 # 比重
  python calc_verify.py --mode prop-change --w 0.021 --a 0.0573 --b 0.0092  # 两期比重差
  python calc_verify.py --mode avg-rate --a 0.695 --b 0.252        # 平均数增长率
  python calc_verify.py --mode base-prop --A 609.0 --B 2582.0 --a 0.161 --b 0.122  # 基期比例
  python calc_verify.py --mode expr --expr "2582.0*1.122/1.161"    # 任意算式
"""
import argparse
import sys

def f(x, nd=4):
    """格式化：大数给千分位，小数给4位有效"""
    if abs(x) >= 1000:
        return f"{x:,.2f}"
    return f"{x:.6g}"

def pct(x):
    return f"{x*100:.4g}%"

def main():
    p = argparse.ArgumentParser(description="资料分析精确计算验证器")
    p.add_argument("--mode", required=True, help="base|growth-amt|growth-amt2|rate|rate2|interval|mix|avg|avg-amt|proportion|prop-change|avg-rate|base-prop|expr")
    p.add_argument("--cur", type=float, help="现期量")
    p.add_argument("--base", type=float, help="基期量")
    p.add_argument("--rate", type=float, help="增长率(小数)")
    p.add_argument("--delta", type=float, help="增长量")
    p.add_argument("--r1", type=float, help="前期增长率")
    p.add_argument("--r2", type=float, help="后期增长率")
    p.add_argument("--a", type=float, help="分子增长率a / 混合增长率a")
    p.add_argument("--b", type=float, help="分母增长率b / 混合增长率b")
    p.add_argument("--wa", type=float, help="混合部分A的量")
    p.add_argument("--wb", type=float, help="混合部分B的量")
    p.add_argument("--w", type=float, help="现期比重(小数)")
    p.add_argument("--A", type=float, help="分子现期量")
    p.add_argument("--B", type=float, help="分母现期量")
    p.add_argument("--part", type=float, help="部分量")
    p.add_argument("--whole", type=float, help="整体量")
    p.add_argument("--years", type=int, help="年份差n")
    p.add_argument("--expr", type=str, help="任意算式")
    args = p.parse_args()

    m = args.mode
    try:
        if m == "base":
            r = args.cur / (1 + args.rate)
            print(f"基期量 = {f(args.cur)} / (1+{args.rate}) = {f(r)}")
        elif m == "growth-amt":
            # 增长量 = 现期/(1+r)*r ；百化分对照：r=1/n → 现期/(n+1)
            r = args.cur * args.rate / (1 + args.rate)
            n = round(1 / args.rate) if args.rate else 0
            print(f"增长量 = {f(args.cur)}×{args.rate}/(1+{args.rate}) = {f(r)}")
            print(f"[百化分对照] r≈1/{n} → 现期/(n+1) = {f(args.cur/(n+1))}")
        elif m == "growth-amt2":
            r = args.base * args.rate
            print(f"增长量 = {f(args.base)}×{args.rate} = {f(r)}")
        elif m == "rate":
            r = args.cur / args.base - 1
            print(f"增长率 = {f(args.cur)}/{f(args.base)} - 1 = {pct(r)}")
        elif m == "rate2":
            r = args.delta / (args.cur - args.delta)
            print(f"增长率 = 增长量/(现期-增长量) = {f(args.delta)}/{f(args.cur-args.delta)} = {pct(r)}")
        elif m == "interval":
            r = args.r1 + args.r2 + args.r1 * args.r2
            print(f"间隔增长率 = r1+r2+r1×r2 = {args.r1}+{args.r2}+{f(args.r1*args.r2)} = {pct(r)}")
            print(f"间隔倍数 = (1+r1)(1+r2) = {f((1+args.r1)*(1+args.r2))}")
        elif m == "mix":
            # 加权混合增长率（a、b 用百分数数值如 4.6 表示 4.6%）
            wa, wb = args.wa, args.wb
            r = (args.a * wa + args.b * wb) / (wa + wb)
            print(f"混合增长率 = ({args.a}×{f(wa)} + {args.b}×{f(wb)}) / {f(wa+wb)} = {r:.4f}%")
            print(f"验证：居中不正中，介于 {min(args.a,args.b)}% 与 {max(args.a,args.b)}% 之间 ✓")
        elif m == "avg":
            ratio = args.cur / args.base
            r = ratio ** (1.0 / args.years) - 1
            print(f"年均增长率：({f(args.cur)}/{f(args.base)})^(1/{args.years}) - 1")
            print(f"  总倍数 = {f(ratio)}  →  年均增长率 = {pct(r)}")
            print(f"  [秒杀对照] 总倍数≈{ratio:.3f}，查幂次方表反推 r 的范围")
        elif m == "avg-amt":
            r = (args.cur - args.base) / args.years
            print(f"年均增长量 = ({f(args.cur)}-{f(args.base)})/{args.years} = {f(r)}")
        elif m == "proportion":
            r = args.part / args.whole
            print(f"比重 = {f(args.part)} / {f(args.whole)} = {pct(r)}")
        elif m == "prop-change":
            # 两期比重差 = w × (a-b)/(1+a)
            d = args.w * (args.a - args.b) / (1 + args.a)
            print(f"比重差 = {f(args.w)}×({args.a}-{args.b})/(1+{args.a}) = {d*100:.4f} 个百分点")
            print(f"[秒杀对照] 必小于 |a-b| = {abs(args.a-args.b)*100:.4g} 个百分点")
        elif m == "avg-rate":
            r = (args.a - args.b) / (1 + args.b)
            print(f"平均数增长率 = (a-b)/(1+b) = ({args.a}-{args.b})/(1+{args.b}) = {pct(r)}")
            print(f"[秒杀对照] 直接比较时只看 (a-b) = {f(args.a-args.b)}")
        elif m == "base-prop":
            r = args.A / args.B * (1 + args.b) / (1 + args.a)
            print(f"基期比例 = A/B × (1+b)/(1+a) = {f(args.A/args.B)} × {f((1+args.b)/(1+args.a))} = {pct(r)}")
        elif m == "expr":
            # 仅允许数字与安全运算符
            allowed = set("0123456789.+-*/() %")
            e = args.expr.replace(" ", "")
            if not e or not set(e) <= allowed:
                print("错误：表达式含非法字符（仅支持数字 + - * / ( ) %）")
                sys.exit(1)
            val = eval(e, {"__builtins__": {}}, {})
            print(f"{args.expr} = {f(val)}")
        else:
            print(f"未知模式：{m}")
            sys.exit(1)
    except ZeroDivisionError:
        print("错误：除数为0，检查参数")
        sys.exit(1)
    except AttributeError as e:
        print(f"参数缺失：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
