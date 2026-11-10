<div align="center">

<!-- Animated Header -->
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:58a6ff,100:1f6feb&height=220&section=header&text=DCDannyCheung&fontSize=75&fontColor=ffffff&fontAlignY=38&desc=%20&animation=twinkling" />

<!-- Typing SVG -->
<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=58A6FF&center=true&vCenter=true&random=false&width=600&lines=%F0%9F%91%8B+Hello%2C+I'm+DCDannyCheung;%F0%9F%9A%80+Welcome+to+my+GitHub;%F0%9F%92%BB+Always+learning%2C+always+building;%E2%9C%A8+Let's+create+something+amazing" alt="Typing SVG" />
</a>

<!-- Snake Animation -->
<img width="100%" src="https://github.com/DCDannyCheung/DCDannyCheung/raw/output/github-snake-dark.svg" alt="Snake animation" />

</div>

---

<!-- Orbit Animation -->
<div align="center">

## 🛰️ Kepler Elliptical Orbit

<img src="orbit-animation.gif" width="520" alt="Kepler Elliptical Orbit Animation" />

**正在学习：轨道方程 (Orbital Equations)**

| 公式 | 说明 |
|:----:|:----:|
| `r = a(1 - e²) / (1 + e·cos ν)` | 轨道方程 — 真近点角 ν 到轨道半径 r |
| `M = E - e·sin E` | 开普勒方程 — 平近点角 M ↔ 偏近点角 E |
| `tan(ν/2) = √((1+e)/(1-e)) · tan(E/2)` | 近点角变换 — 偏近点角 E → 真近点角 ν |
| `v = √(μ(2/r - 1/a))` | 活力公式 (Vis-Viva) — 瞬时速度 v |
| `T = 2π√(a³/μ)` | 开普勒第三定律 — 轨道周期 T |

动画演示了开普勒第二定律（等面积定律）：卫星在近日点速度最快，在远地点速度最慢。

**🛠️ 生成方式**

用 Python + matplotlib 从轨道方程直接求解并渲染，源码在 [`generate_orbit_gif.py`](generate_orbit_gif.py)：

```python
# 1) 数值求解开普勒方程 M = E - e·sin(E)（Newton-Raphson）
E = solve_kepler(M, e)

# 2) 由偏近点角变换得真近点角
nu = 2 * arctan2(sqrt(1+e)·sin(E/2), sqrt(1-e)·cos(E/2))

# 3) 轨道方程求半径，再转直角坐标
r = a(1-e²) / (1 + e·cos(nu))
x, y = r·cos(nu), r·sin(nu)
```

参数：半长轴 `a = 1.0`、离心率 `e = 0.5`。改这两个值就能生成不同轨道。

</div>

---

<!-- About Section -->
## 🧑‍💻 About Me

```yaml
name: DCDannyCheung
location: 🌏 China
current_focus: Orbital mechanics & Kepler's laws
code_motto: "Code is poetry, keep it clean."
hobbies: [coding, orbital mechanics, gaming, exploring new tech]
```

---

<!-- Tech Stack -->
## 🛠️ Tech Stack

<table>
<tr>
<td align="center" width="50%">

### 💻 Languages

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<br/>
<img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" alt="C++" />

</td>
<td align="center" width="50%">

### ⚙️ Frameworks & Tools

<img src="https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" alt="Vue.js" />
<br/>
<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git" />

</td>
</tr>
</table>

---

<!-- GitHub Stats -->
## 📊 GitHub Stats

<div align="center">

<img height="170" src="https://github-readme-stats.vercel.app/api?username=DCDannyCheung&show_icons=true&theme=tokyonight&include_all_commits=true&count_private=true&hide_border=true&bg_color=0d1117&title_color=58a6ff&icon_color=1f6feb&text_color=c9d1d9" alt="GitHub Stats" />

<img height="170" src="https://github-readme-streak-stats.herokuapp.com?user=DCDannyCheung&theme=tokyonight&hide_border=true&background=0D1117&ring=58A6FF&fire=1F6FEB&currStreakLabel=58A6FF&sideLabels=C9D1D9&dates=C9D1D9&currStreakNum=C9D1D9" alt="GitHub Streak" />

<img height="170" src="https://github-readme-stats.vercel.app/api/top-langs/?username=DCDannyCheung&layout=compact&theme=tokyonight&hide_border=true&bg_color=0d1117&title_color=58a6ff&text_color=c9d1d9" alt="Top Languages" />

<!-- Activity Graph -->
<img width="95%" src="https://github-readme-activity-graph.vercel.app/graph?username=DCDannyCheung&theme=github-compact&hide_border=true&bg_color=0d1117&color=58a6ff&line=1f6feb&point=c9d1d9" alt="Activity Graph" />

</div>

---

<!-- Trophies -->
## 🏆 GitHub Trophies

<div align="center">

<img src="https://github-profile-trophy.vercel.app/?username=DCDannyCheung&theme=algolia&no-border=true&no-bg=true&margin-w=8&margin-h=8&row=2" alt="Trophies" />

</div>

---

<!-- Connect With Me -->
## 🤝 Connect With Me

<div align="center">

<a href="https://github.com/DCDannyCheung">
  <img src="https://img.shields.io/badge/GitHub-DCDannyCheung-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
</a>

</div>

---

<!-- Profile Views Counter -->
<div align="center">

<img src="https://komarev.com/ghpvc/?username=DCDannyCheung&label=Profile%20Views&color=58a6ff&style=for-the-badge&label=Visitors" alt="Profile Views" />

</div>

---

<!-- Footer -->
<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:58a6ff,100:1f6feb&height=120&section=footer" />

</div>

<!-- Little secret -->
<!-- 💙 Thanks for scrolling all the way down -->
