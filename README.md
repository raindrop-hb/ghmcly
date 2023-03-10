# 工商银行萌宠乐园

<p align="center">
    <a href="https://github.com/raindrop-hb"><img alt="Author" src="https://img.shields.io/badge/author-raindrop-blueviolet"/></a>
    <img alt="PHP" src="https://img.shields.io/badge/code-Python-success"/>
    <img src="https://github-visitor-badge.glitch.me/badge?page_id=ghmcly"/>
</p>

可直接部署在华为云函数流

必填参数push，token，多个token一定要带引号和逗号

函数执行入口填：index.main_handler

触发器用定时触发器-cron表达式：0 30 08 * * ?

每天8:30执行
