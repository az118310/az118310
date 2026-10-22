# Python 速查表（写给"基本忘光了"的你）

> 用法：卡住时先查这里。**不要通读**——按需查，用多了自然记住。
> 每一节末尾有「你的项目里哪句话用了它」，把语法和真实场景挂钩才记得住。

---

## 0. 变量与类型

```python
name = "小圆脸的日常"      # str  字符串，用引号
price = 189.0              # float 浮点数，带小数
count = 10                 # int   整数
is_pending = True          # bool  布尔，True / False
nothing = None              # NoneType 空值（不是 0，也不是 ""）
```

**判断类型**：
```python
type(x)              # 打印类型
isinstance(x, str)   # 判断是不是字符串，面试常问
```

**类型转换**：
```python
int("189")           # 字符串 → 整数，189
str(189)             # 数字 → 字符串，"189"
float("189.5")       # 字符串 → 浮点数
```

> ⚠️ `int("abc")` 会抛 `ValueError`。真实场景：工单里价格可能是 `"189元"` 这种脏数据，
> 需要先清洗。**这正是"防御性代码"的由来。**

---

## 1. 列表 list（有序可变）

```python
tickets = [t1, t2, t3]      # 创建
tickets = []                 # 空列表
tickets[0]                   # 第一个
tickets[-1]                  # 最后一个
tickets[0:3]                 # 前三个（左闭右开，不含索引3）
tickets[0:3]                 # 等价于 tickets[:3]
tickets[1:3]                 # 索引1和2
tickets[-2:]                 # 最后两个
len(tickets)                 # 长度
"key" in tickets             # 成员判断 → True/False
```

**常用方法**：
```python
tickets.append(item)         # 末尾追加（最常用）
tickets.extend([a, b])       # 追加多个
tickets.remove(item)         # 删除指定元素（值不存在会报错）
tickets.pop()                # 弹出最后一个，返回被弹出的值
tickets.sort()               # 排序（默认按元素本身）
tickets.sort(key=lambda x: x["price"])   # 按字典某个字段排序
```

**列表推导式**（Pythonic 写法）：
```python
# 普通写法
result = []
for t in tickets:
    if t["status"] == "pending":
        result.append(t)

# 推导式写法（等价）
result = [t for t in tickets if t["status"] == "pending"]
```

> **你的项目里**：`pending = [t for t in tickets if t["status"] == "pending"]`
> 面试常问「为什么用推导式」——答：可读性好、少写循环样板、Python 社区惯例。

---

## 2. 字典 dict（键值对，无序）

```python
ticket = {
    "id": "T20261001001",
    "customer": "小圆脸的日常",
    "price": 189.0,
    "intent": "size_advice",
}
```

**取值与判断**：
```python
ticket["id"]              # 取值，键不存在 → KeyError（程序崩）
ticket.get("id")          # 取值，键不存在 → None（不崩）
ticket.get("id", "未知")   # 取值，键不存在 → 返回默认值
"id" in ticket            # 键是否存在
```

**遍历**：
```python
for key in ticket:                    # 遍历键
for value in ticket.values():         # 遍历值
for key, value in ticket.items():     # 遍历键值对（最常用）
```

**计数器的标准写法**（你会天天用）：
```python
counts = {}
for t in tickets:
    key = t["intent"]
    counts[key] = counts.get(key, 0) + 1
```
> 等价写法：`collections.Counter(t["intent"] for t in tickets)`

**修改与新增**：
```python
ticket["status"] = "replied"    # 修改（键不存在会新增）
ticket.update({"status": "replied", "note": "已处理"})
del ticket["note"]              # 删除键
ticket.pop("note", None)        # 删除并返回，键不存在不报错
```

> **你的项目里**：意图统计、每条工单的字段读取，全靠字典。

---

## 3. 条件 if / elif / else

```python
if t["status"] == "pending":
    print("待处理")
elif t["status"] == "replied":
    print("已回复")
else:
    print("其他")
```

**常见坑**：
| 坑 | 后果 | 正确 |
|---|---|---|
| `=` 写成 `==` | 赋值，不是比较，逻辑永远成立 | 判断相等用 `==` |
| `status = "pending"` | 把变量改了 | `status == "pending"` |
| 字符串用 `=` 比较 | 永远 False | 字符串用 `==` |

**真值判断**（Python 特色）：
```python
if t["message"]:              # 非空字符串 → True
if not t["notes"]:            # None / "" / [] / 0 → True
if t["price"] > 0 and t["status"] == "pending":
```

---

## 4. 循环 for / while

```python
for t in tickets:             # 遍历列表
    print(t["id"])

for i, t in enumerate(tickets):  # 带下标
    print(i, t["id"])

for k, v in ticket.items():      # 遍历字典
    print(k, v)

for i in range(5):           # 0 1 2 3 4
for i in range(2, 10, 2):    # 2 4 6 8

while True:                 # 条件循环（慎用，容易死循环）
    if done:
        break
```

**控制语句**：
```python
break       # 跳出整个循环
continue    # 跳过本次，进入下一轮
```

> ⚠️ **缩进是语法，不是风格。** Python 用缩进表示代码块。
> `if` / `for` 下面的代码必须缩进 4 个空格，缩进错了直接 `IndentationError`。

---

## 5. 函数

```python
def 函数名(参数, 默认值=None):
    """文档字符串（写清楚这个函数干什么，面试加分）"""
    函数体
    return 结果
```

**调用**：
```python
result = count_by(tickets, "intent")
result = count_by(tickets, field="intent")     # 关键字调用
```

**默认值 + 可变参数**：
```python
def f(a, b=10):              # b 有默认值
def f(a, *args, **kwargs):   # 不定个数参数
    # args 是元组，kwargs 是字典
```

**返回多个值**：
```python
def stats(tickets):
    return len(tickets), 189.0     # 返回元组
n, avg = stats(tickets)            # 解包
```

**类型注解**（建议写，不影响运行）：
```python
def count_by(tickets: list, field: str) -> dict:
```

---

## 6. 文件读写

```python
# 读整个文件 → 字符串
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 逐行读
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

# 写文件（覆盖）
with open(path, "w", encoding="utf-8") as f:
    f.write("hello")

# 追加
with open(path, "a", encoding="utf-8") as f:
    f.write("more")
```

**三个必须的细节**：
1. `encoding="utf-8"` —— 不写 Windows 按 GBK 读，中文乱码
2. `with` —— 自动关闭文件，异常时也关
3. `"w"` 会**清空原文件**，"a" 才追加。写错了数据就没了。

---

## 7. JSON

```python
import json

# JSON 文本 → Python 对象
data = json.loads(text)

# Python 对象 → JSON 文本
text = json.dumps(data, ensure_ascii=False, indent=2)

# 配合文件
with open(path, "r", encoding="utf-8") as f:
    data = json.loads(f.read())

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

**`ensure_ascii=False` 不写会怎样**：中文变成 `\u5c0f\u5706\u8138`，可读性极差。
**`indent=2` 不写会怎样**：全部挤成一行，看不下去。

---

## 8. 异常处理

```python
try:
    risky_operation()
except FileNotFoundError:       # 文件不存在
    print("文件不存在")
except json.JSONDecodeError as e:   # JSON 格式错
    print(f"格式错误: {e}")
except Exception as e:          # 兜底（尽量少用）
    print(f"未知错误: {e}")
finally:
    cleanup()                   # 一定执行
```

**常见异常类型**：
| 异常 | 什么时候触发 |
|---|---|
| `FileNotFoundError` | 文件路径不存在 |
| `JSONDecodeError` | JSON 格式错误 |
| `KeyError` | 字典键不存在（用 `[]` 取值时） |
| `IndexError` | 列表下标越界 |
| `ValueError` | 类型转换失败（`int("abc")`） |
| `TypeError` | 类型不兼容 |

> **你的项目里**：`load_tickets_safe()` 就是这个模式。
> 面试会问「为什么不用 try/except Exception 全包」——答：**要精准捕获**，
> 全包会掩盖真正的 bug。

---

## 9. 常用内置函数

```python
len(x)              # 长度
sum(numbers)        # 求和
max(nums) / min(nums)
sorted(nums)        # 排序返回新列表
sorted(nums, key=lambda x: x["price"])   # 按字段排序
round(3.14159, 2)   # 四舍五入
abs(-5)
str(123) / int("123") / float("1.5")
any([False, True])  # 有 True 就是 True
all([True, True])   # 全 True 才是 True
enumerate()         # 遍历带下标
zip([1,2],[3,4])    # 并行遍历 → [(1,3),(2,4)]
```

---

## 10. 最容易犯的 5 个错（对照自查）

| # | 错误 | 后果 | 记住 |
|---|---|---|---|
| 1 | `=` 和 `==` 混用 | 逻辑永远为真，静默出错 | `=` 赋值，`==` 比较 |
| 2 | 缩进用了 Tab 或不一致 | `IndentationError` | 统一 4 空格 |
| 3 | 忘记 `encoding="utf-8"` | 中文乱码 | 每个 open 都写 |
| 4 | `json.dump` 忘 `ensure_ascii=False` | 中文变 `\uXXXX` | 写文件必加 |
| 5 | 用了未定义的变量 | `NameError` | 报错信息里有变量名，照着查 |

---

## 11. 读报错信息的正确姿势

报错信息**从下往上**看：

```
Traceback (most recent call last):
  File "step1_basics.py", line 42, in <module>
    print(t[customer])
          ^
NameError: name 'customer' is not defined
```

**三步定位法**：
1. **最后一行** = 异常类型 + 原因（`NameError: name 'customer' is not defined`）
2. **`^` 标记的位置** = 出错的那一列
3. **`line 42`** = 出错的行号

常见异常 → 原因速查：
- `NameError: name 'x' is not defined` → 变量名拼错 / 没定义 / 忘了引号
- `KeyError: 'xxx'` → 字典里没这个键 → 改用 `.get()`
- `IndexError: list index out of range` → 下标越界 → 检查 `len()`
- `TypeError: ... not subscriptable` → 类型不对，比如给 str 用了 `[0]`（那是字符）
- `IndentationError` → 缩进问题
- `SyntaxError` → 语法写错了，看 `^` 指的位置
- `ModuleNotFoundError: No module named 'xxx'` → 包没装 / 用错解释器

---

## 12. 调试三招

1. **print 大法**（最朴素也最有效）
   ```python
   print(f"DEBUG: t = {t}, type = {type(t)}")
   ```
2. **断点**（VSCode）：行号左边点一下 → F5 → 在 `Debug Console` 看变量
3. **最小复现**：把 200 行代码删到 10 行还能复现 → 问题在这 10 行里

> **别一上来就 print 打印整个对象**，数据一多刷屏。打印你怀疑的那一个变量。

---

## 附：今天这两个文件的对应关系

| 语法点 | 在 step1/step2 的位置 |
|---|---|
| 字典取值 `t["intent"]` | 读工单字段 |
| 列表推导式 | 筛选 pending |
| 字典计数器 | 统计意图分布 |
| `for ... in` | 遍历所有工单 |
| `if` + `==` | 判断 status |
| 函数 + `**kwargs` | `filter_by` 多条件筛选 |
| `json.loads` / `json.dump` | 读数据 / 写日报 |
| `with open(...)` | 文件读写 |
| `try/except` | `load_tickets_safe` |
| f-string `f"{x:.2f}"` | 金额格式化 |

**这张表就是你今天的收获清单。跑通两个文件后，它们会变成你的肌肉记忆。**
