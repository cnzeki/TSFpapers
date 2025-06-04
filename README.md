## A tool for TimeSeries research

![TSFpaper](https://img.shields.io/github/stars/ddz16/TSFpaper)

### Init 

Check out paper list from [ddz16/TSFpaper](https://github.com/ddz16/TSFpaper)

~~~
git clone  https://github.com/ddz16/TSFpaper src
~~~

### Update all

windows: run `update.bat`
linux: run `update.sh`

### Run script with args

| param    | default          | comment                      |
| -------- | ---------------- | ---------------------------- |
| input    | "paperlist.xlsx" | extracted paper list table   |
| output   | "pdf"            | directory to download papers |
| category | None             |                              |

~~~python
python downloader.py
~~~
This will download all papers in the `output` directory and gen a  `output.xlsx` to navigate.

