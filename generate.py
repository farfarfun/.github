"""生成组织主页 README 的旧脚本。

⚠️ `profile/README.md` 现在是**手工维护**的（2026-08-26 按 far* 工具链 / fun* 领域库
两条线重写，44 个链接逐个验证过）。本脚本的产出基于下面那份写死的 9 个包的列表，
信息量远低于手工版本。

以前这个文件在模块末尾直接调用 generate()，`python generate.py` 一跑就把手工版本
覆盖掉。现在默认只写 profile/README.generated.md 供对比，要覆盖正式主页必须显式
传 --force。
"""

import argparse
import os

import pandas as pd

data = """
## Hi 

<p align="center">
<a href="https://github.com/farfarfun">
    <img src="https://readme-typing-svg.demolab.com?font=Georgia&size=18&duration=2000&pause=100&multiline=true&width=500&height=80&lines=farfarun;活到老+%7C+学到老+%7C+玩到老;牛哥永远都不老" alt="Typing SVG" />
</a>

<br/>
<a href="https://github.com/farfarfun">
    <img src="https://img.shields.io/badge/Website-farfarfun-red?style=flat-square">
</a>  

<a href="mailto:farfarfun@qq.com">
    <img src="https://img.shields.io/badge/Email-farfarfun@qq.com-red?style=flat-square&logo=gmail&logoColor=white">
</a>

<a href="https://pypi.org/user/niuliangtao/">
    <img src="https://img.shields.io/badge/PyPi-niuliangtao-blue?style=flat-square&logo=pypi&logoColor=white">
</a>
<br/>

<a href="https://github.com/farfarfun">
    <img src="https://github-stats-alpha.vercel.app/api?username=farfun&cc=22272e&tc=37BCF6&ic=fff&bc=0000&count_private=true&include_all_commits=true&orgs=farfarfun">
</a>

"""


class GenerateReadMe:
    def __init__(self, org_name="farfarfun"):
        self.org_name = org_name
        self.text = data

    def generate(self, force=False):
        self.user_stat()
        self.language_of_code()
        self.organize_view_stat()
        self.generate_package()
        here = os.path.dirname(os.path.abspath(__file__))
        name = "profile/README.md" if force else "profile/README.generated.md"
        readme_path = os.path.join(here, name)
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(self.text)
        if force:
            print(f"已覆盖手工维护的组织主页: {readme_path}")
        else:
            print(f"已写入 {readme_path}（未动 profile/README.md）")
            print("确认要用生成内容覆盖手工维护的主页，再加 --force 重跑。")

    def generate_package(self):
        rows = [
            {
                "title": f"[{self.org_name}](https://github.com/{self.org_name})",
                "stars": f'<img alt="Stars" src="https://img.shields.io/github/stars/{self.org_name}?style=flat-square&labelColor=black"/>',
                "forks": f'<img alt="Followers" src="https://img.shields.io/github/followers/{self.org_name}?style=flat-square&labelColor=black"/>',
                "watchers": "",
            }
        ]

        rows.clear()
        packages = [
            "fundrive",
            "funrec",
            "fundata",
            "funbuild",
            "funcoin",
            "funread",
            "funget",
            "funutil",
            "funtable",
        ]
        for package in packages:
            rows.append(
                {
                    "title": f"[{package}](https://github.com/{self.org_name}/{package})",
                    "stars": f'<img alt="Stars" src="https://img.shields.io/github/stars/{self.org_name}/{package}?style=flat-square&labelColor=black"/>',
                    "forks": f'<img alt="Forks" src="https://img.shields.io/github/forks/{self.org_name}/{package}?style=flat-square&labelColor=black"/>',
                    "watchers": f'<img alt="Watchers" src="https://img.shields.io/github/watchers/{self.org_name}/{package}?style=flat-square&labelColor=black"/>',
                    "download": f"[![{package}](https://static.pepy.tech/personalized-badge/{package}?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/{package})",
                    "download-month": f"![{package}](https://img.shields.io/pypi/dm/{package})",
                    "version": f"![PyPI - Version](https://img.shields.io/pypi/v/{package})",
                    "format": f"![PyPI - Format](https://img.shields.io/pypi/format/{package})",
                    "pypi": f"[![SQLPyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/{package})",
                }
            )
        self.text += "\n" * 3
        self.text += pd.DataFrame(rows).to_markdown()

    def organize_view_stat(self):
        self.text += """
<br>
<div align="center">
  <img alt="Profile Views" src="https://komarev.com/ghpvc/?username=farfarfun&label=Profile%20views&style=aura&color=5865F2">  
</div>
<br>
        """

    def language_of_code(self):
        self.text += """
|Repo | Commit |
|--|--|
| ![](http://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=farfun&theme=dracula)  | ![](http://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=farfun&theme=dracula) |
        """

    def user_stat(self):
        self.text += """![](http://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=farfun&theme=dracula)"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="用生成内容覆盖手工维护的 profile/README.md（默认只写 README.generated.md）",
    )
    GenerateReadMe(org_name="farfarfun").generate(force=parser.parse_args().force)
