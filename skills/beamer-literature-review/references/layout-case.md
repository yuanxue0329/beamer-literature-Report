# 案例：纵向拼接图重排为双栏

## 材料与目标

假设一张纵向拼接图包含系统框图、平台照片和任务执行过程。整张图按幻灯片高度缩小时，图内文字和照片会变得难以辨认。

先读取像素尺寸、长宽比与物理尺寸信息，并查看各子图的实际分界。可以把系统／平台部分与执行过程分别通过 TeX 裁切显示，再排成横向两栏。

## 布局判断

1. 确认两块内容各自包含完整子图、图例和必要标签。
2. 根据裁切后的长宽比设置两栏比例，两栏不必等宽。
3. 将图片放大到标题与页脚之间的主体区域，再安排短图注和必要说明。
4. 如果普通正文边距仍有可用空白，可以调整图像位置或加宽图片区域，但要检查实际边界和相邻列。

下面的骨架不预设负偏移和裁切量。`images/composite.jpg` 为使用者自己的原图，仓库不提供该素材。

```latex
\begin{frame}
    \frametitle{系统部署与任务执行}
    \footnotesize
    \begin{columns}[c,onlytextwidth]
        \begin{column}{0.48\textwidth}
            \begin{figure}
                \centering
                % 先根据实际子图边界设置 trim，顺序：左、下、右、上。
                \includegraphics[width=\linewidth,keepaspectratio,
                    trim=0bp 0bp 0bp 0bp,clip]{images/composite.jpg}
            \end{figure}
        \end{column}
        \begin{column}{0.49\textwidth}
            \begin{figure}
                \centering
                % 对同一原图显示另一个完整子图区域。
                \includegraphics[width=\linewidth,keepaspectratio,
                    trim=0bp 0bp 0bp 0bp,clip]{images/composite.jpg}
            \end{figure}
        \end{column}
    \end{columns}
    {\scriptsize 左：系统与平台；右：任务执行过程。图注按原文提炼。\par}
    \begin{itemize}
        \item 说明系统各模块之间的输入、输出与反馈。
        \item 用简短文字交代任务设置和主要观察。
    \end{itemize}
\end{frame}
```

`0.48`、`0.49` 只让示例成为合法的常规分栏，不是最终版式。图片的裁切量、列宽、最大高度和偏移量都需要根据实际内容调整。

## 需要保留的经验

- 两列各占 `0.55\textwidth`、再配合 `\hspace*{-0.6cm}`，可能适用于某张已经调试过的页面，但不自动适用于其他图片或模板。
- 同时指定宽高上限并使用 `keepaspectratio` 时，若宽度已受限，仅增加高度不会继续放大图像。
- 分清图片内部白边与正文外侧边距；先减少无用图片边缘，再利用页面空间。
- 完整幻灯片截图中的标题和页脚也会进入非白像素包围框，不能据此自动裁掉它们。
- 使用 `\textbf{...}`、`\hspace*{...}` 和 `Fig.~1--3` 等合法 LaTeX，不把聊天 Markdown 标记带入源码。

单位换算、布局边界和更多版式决策见 [layout-recipes.md](layout-recipes.md)。
