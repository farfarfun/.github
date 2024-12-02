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

    def generate(self):
        self.user_stat()
        self.language_of_code()
        self.organize_view_stat()
        self.generate_package()
        current_file_path = os.path.abspath(__file__)
        readme_path = os.path.join(os.path.dirname(current_file_path), "profile/README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(self.text)

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
            "fundata",
            "funsecret",
            "funbuild",
            "funcoin",
            "funread",
            "funget",
            "funutil",
            "funkeras",
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


GenerateReadMe(org_name="farfarfun").generate()
