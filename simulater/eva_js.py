# -*- coding: utf-8 -*-

"""
# 代码参考https://www.jianshu.com/p/609c39702814，https://blog.csdn.net/Chen_chong__/article/details/82950968
# js部分直接参照参考
"""

js1 = '''() =>{
           Object.defineProperties(navigator,{
             webdriver:{
               get: () => false
             }
           })
        }'''

js2 = '''() => {
            alert (
            window.navigator.webdriver
            )
        }'''

js3 = '''() => {
            window.navigator.chrome = {
            runtime: {},
            // etc.
            };
        }'''

js4 = '''() =>{
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        }'''

js5 = '''() =>{
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5,6],
            });
        }'''