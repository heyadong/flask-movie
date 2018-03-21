<h3>这是一个用FLask 搭建的微电影网站</h3>

day1 2018-3-20：


使用vue.js 添加css 样式：


vue.js 结构：


 var = new Vue({
 
     delimiters:['${','}'],
     el: #app,
     data:{
     isactive:true
     site:"baidu.com"
     },
     methods:{
         function1: function(){
             return this.site
          },
          function2: function(){
              return null     
          },
         },       
 })
 
 
 delimiters: 更改转义字符 delimiters:['${','}'] Vue.js默认转义字符是{{ }},与jinja2的默认转义字符相同，
 
 前后端未完全分离会导致错误的转义， 使用delimiters将Vue.js的转义字符更改为 ${ }.
 
 el: 标签的id,注意id前面的
 
 data: 数据
 
 methods：函数
 
"{<div id='app' class="list-group-item" v-bind:class="{active:isactive}"> </div>}"

使用v-bind指令 当isactive==true 将给div添加一个active 样式相当于：

"{<div id='app' class="list-group-item active"> </div>}"
