# Beamer Literature Report

**面向 LaTeX Beamer 文献综述与科研汇报的 Codex Skill。**

先检查图片的像素尺寸、长宽比、有效内容与白边，再决定裁切、缩放、分栏或分页。在保留标题、校徽和页脚的前提下，让论文图表在幻灯片主体区域中清晰可读。

技能名称：`beamer-literature-review`。仓库名称与技能名称可以不同。

## 适用场景

- 使用已有 Beamer 模板整理论文、组会汇报与文献综述。
- 将论文流程图、实验截图与结果表组织为连贯的报告。
- 处理纵向拼接图、密集表格、双栏图片和较大的页面白边。
- 保留原模板与用户修改，用简单 LaTeX 代码继续编辑。

## 核心做法

1. **先读现有文件。**读取最新 `.tex`、主题、图片和项目要求，保留已经调试过的布局。
2. **先看图再排版。**尺寸检查与目视判断配合，确认图内小字、图例、坐标轴和裁切边界。
3. **尽量放大有效内容。**先减少图片内的无用白边，再利用合适的主体区域；偏移量和列宽按具体页面调整。
4. **保留科学含义。**图注忠实概括原文，数据保留实验条件，不混淆仿真、实机、推理与规划时间。
5. **保持源码易改。**优先使用 `columns`、`itemize`、`enumerate`、`block`、`tabular` 与显式分页。

`0.55\textwidth`、`-0.6cm` 等数值只可能是某页的调试结果，不是适用于所有图片的默认参数。

## 安装到 Codex

### 方式一：使用 skill-installer

在提供 `$skill-installer` 的 Codex 环境中输入：

```text
使用 $skill-installer 安装这个技能：
https://github.com/yuanxue0329/beamer-literature-Report/tree/main/skills/beamer-literature-review
```

### 方式二：手动安装（Windows PowerShell）

```powershell
git clone https://github.com/yuanxue0329/beamer-literature-Report.git
Set-Location beamer-literature-Report

$skillRoot = Join-Path $env:USERPROFILE '.codex\skills'
if ($env:CODEX_HOME) {
    $skillRoot = Join-Path $env:CODEX_HOME 'skills'
}
$skillDestination = Join-Path $skillRoot 'beamer-literature-review'
if (Test-Path -LiteralPath $skillDestination) {
    throw '同名技能已存在。请先备份并决定如何更新，避免覆盖个人修改。'
}
New-Item -ItemType Directory -Path $skillRoot -Force | Out-Null
Copy-Item -LiteralPath '.\skills\beamer-literature-review' -Destination $skillDestination -Recurse
```

安装后，在新一轮对话中调用 `$beamer-literature-review`。不同客户端的技能发现方式以其当前版本为准。

## 使用示例

### 先整理大纲

```text
使用 $beamer-literature-review，先为这些论文拟定汇报大纲。
沿用项目中的 Beamer 模板，列出每页的标题、主要论点、配图、图注与实验数据来源。
先不要修改 TeX。
```

### 修改已有报告

```text
使用 $beamer-literature-review，按确认后的大纲编辑 ReviewReport.tex。
先读取最新源码，保留前面的内容。图片在 images/ 下。
只修改 TeX，不编译、不生成 PPT。
```

### 调整图片布局

```text
使用 $beamer-literature-review 调整这一页的图像布局。
先查看原图的尺寸、比例、内容和白边，再决定裁切、缩放和两栏的宽度。
保留标题、页脚、图例与标签，尽量放大主体内容，不固定套用负偏移值。
```

引用方式可在请求中指定。技能默认每篇论文在首次出现页列题名、出版情况和 DOI，后续页保留原图表号；当前用户或项目要求始终优先。

## 图片检查脚本

仅在运行辅助脚本时需要 Python 和 Pillow。它只读取图片并输出 JSON，不会裁切或改写原图。

在仓库根目录运行：

```powershell
python -m pip install -r requirements.txt
python -X utf8 skills/beamer-literature-review/scripts/inspect_images.py './images/figure.jpg'
python -X utf8 skills/beamer-literature-review/scripts/inspect_images.py './images' --recursive
```

输出包括：

- 实际图片编码、像素尺寸、显示方向与长宽比。
- 依据近白背景估计的内容包围框和外侧裁切候选。
- 图片声明的 DPI；缺失时保留空值。
- 在 DPI 有效时计算的候选 `bp` 裁切量，仍需与 TeX 自然尺寸核对。

**白边候选不能代替目视判断。**浅色标记、透明背景、图注、图例及压缩噪声均可能影响结果。像素不能在缺少物理尺寸依据时直接当成 TeX 的 `bp`。

脚本默认扫描目录的直接子文件；加 `--recursive` 扫描子目录。`--white-threshold` 可调整近白背景阈值，默认为 `245`。

## 文件结构

```text
.
├── README.md
├── LICENSE
├── requirements.txt
└── skills/
    └── beamer-literature-review/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── references/
        │   ├── layout-recipes.md
        │   └── layout-case.md
        └── scripts/inspect_images.py
```

## 默认交付范围

技能默认编辑已有 TeX；编译 PDF、检查新渲染结果或生成其他格式，需要在任务中明确要求。仅检查源码时，不会声称已经确认最终排版。

仓库提供工作方法、代码与文字示例。论文图片、学校标识、个人汇报、字体和完整 Beamer 主题需要使用者自行提供，不随本仓库分发。

## 许可与改进

本仓库原创内容采用 [MIT License](LICENSE)。欢迎通过 Issues 或 Pull Requests 反馈具体的排版问题与改进建议；示例请尽量使用可公开的最小材料。
