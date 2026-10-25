# 按有效内容排版

## 1. 图片检查输出如何使用

`scripts/inspect_images.py` 只读取图片，输出 JSON：

```powershell
python -X utf8 scripts/inspect_images.py './images/figure.jpg'
python -X utf8 scripts/inspect_images.py './images' --white-threshold 245
```

- `pixel_size`、`aspect_ratio`：经 EXIF 方向归一后的尺寸与比例；无方向标记的普通论文截图与原始尺寸相同。
- `content_bbox_px`：非近白像素的包围框，顺序为左、上、右、下，右下边界不包含在框内。
- `suggested_outer_trim_px_lbrt`：由包围框得到的外侧留白，顺序为左、下、右、上。只是估计，不自动应用。
- `outer_margin_area_fraction`：包围框以外面积的比例，不代表图内全部白色区域的比例。
- `declared_dpi`：图片元数据声明的分辨率，不等于已确认的 TeX 自然尺寸；缺失时保留 `null`。
- `trim_bp_from_declared_dpi_lbrt`：仅有有效 DPI 时按该声明换算，仍需核对当前 TeX 引擎使用的自然尺寸。

白底检测适合论文截图。彩色背景、照片、浅色线条、透明图、压缩噪声或完整页面截图都需要人工判断；不要自动删掉浅色图例或把页脚、图注当成无用内容。该脚本不能识别拼接图内部的科学分界。

## 2. 确定实际可用区域

从当前模板或已有预览中确定页面边界、标题栏底线、页脚上沿和校徽区域。为图注及必要文字分配空间后，得到图片可用宽高 \(W_a,H_a\)。可以利用普通正文边距中的空白，但保持图片与说明处于页面内部。

不要把屏幕截图的像素尺寸直接当成纸张尺寸；截图可能包含缩放、边框或裁切。先读 `.tex` 的 `aspectratio`、主题和几何设置。

## 3. 依据裁切后的比例缩放

设原图宽高为 \(W,H\)，裁切左、右、上、下分别为 \(l,r,t,b\)，则：

\[
W_c=W-l-r,\qquad H_c=H-t-b,\qquad q=W_c/H_c.
\]

可用区域内等比放大的尺寸为：

\[
W_d=\min(W_a,qH_a),\qquad H_d=W_d/q.
\]

这解释了常见现象：设置 `width=\linewidth,height=0.55\textheight,keepaspectratio` 后，若宽度已经成为限制，提高 `height` 不会放大图片。应先裁去空白，再调整实际可用宽度或换版式。

`graphicx` 的 `trim` 顺序为 **左、下、右、上**，与常见像素坐标的上／下方向不同。若显示方向一致、图像自然宽高确认为 \(W_n,H_n\) bp，按像素裁切量换算：

\[
(l_{bp},b_{bp},r_{bp},t_{bp})
=\left(l\frac{W_n}{W},b\frac{H_n}{H},r\frac{W_n}{W},t\frac{H_n}{H}\right).
\]

有可确认的 DPI 时，也可按水平、垂直分辨率分别计算 `bp = px × 72 / DPI`。没有 DPI 时，不默认 `1 px = 1 bp`；现有成功的裁切值可以作为同一图片的经验起点。

## 4. 选择图的组织方式

| 图片内容 | 版式决策 |
|---|---|
| 宽流程图 | 横向占满主体宽度，下面保留简短步骤 |
| 单张密集图或原表 | 优先单页放大；必要时移走重复解释 |
| 纵向拼接的多个原图 | 用 TeX 裁切各区域，再横向分栏或显式分页 |
| 两个互补机制 | 两栏分别放图、短图注与一两条说明；列宽可以不等 |
| 半栏结果表与解释 | 左表右文；密集全宽表另外一页 |
| 两表合并后小字不可读 | 保留分开的页面，避免为省页数继续缩小 |

## 5. 位置与列宽的调整

先用正常正文宽度确定内容，再按可用空间适度放大。`onlytextwidth` 不是图片裁切边界，也不会自动保证过宽列不溢出。

对每个内容块检查实际显示边界：

- 水平：`左起点 + 水平偏移` 至 `左起点 + 水平偏移 + 实际宽度`。
- 垂直：图像、图注和文字总高度处于标题栏与页脚之间。
- 相邻列：不相互覆盖，文字不压在图上，必要间隙清楚。

可以使用 `\raggedright` 和 `\hspace*{...}` 调整位置，但不要把负偏移当成固定模板。图片保持在段落中的正常高度范围内；避免通过负垂直间距把内容藏进页脚。

合法的可调结构示例：

```latex
\begin{figure}
    \raggedright
    % 根据本图与当前页面决定是否需要 \hspace*{...}。
    \includegraphics[width=\linewidth,keepaspectratio,
        trim=0bp 0bp 0bp 0bp,clip]{images/figure.jpg}
    \captionsetup{font=scriptsize,skip=3pt}
    \caption{忠实提炼原图，保留原文图号。}
\end{figure}
```

## 6. 根据可用证据判断排版

只有源码与尺寸时，完成有依据的布局估算并说明未编译。已有 PDF 或用户截图时，检查小字、图例、子图边界和标题／页脚距离。若用户授权生成预览，再对目标页迭代调整，不因本技能而自动扩展到整份报告的重排。
