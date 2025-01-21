## A tool for TimeSeries research

![TSFpaper](https://img.shields.io/github/stars/ddz16/TSFpaper)

### Update paper list

~~~
git subtree pull --prefix=data/  https://github.com/ddz16/TSFpaper.git main --squash
~~~

### Download papers

| param    | default          | comment                      |
| -------- | ---------------- | ---------------------------- |
| input    | "paperlist.xlsx" | extracted paper list table   |
| output   | "pdf"            | directory to download papers |
| category | None             |                              |



~~~python
python downloader.py
~~~
This will download all papers in the `output` directory and gen a  `output.xlsx` to navigate.

