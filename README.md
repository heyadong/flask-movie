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
 
<!--"{<div id='app' class="list-group-item" v-bind:class="{active:isactive}"> </div>}"-->

使用v-bind指令 当isactive==true 将给div添加一个active 样式相当于：

<!--"{<div id='app' class="list-group-item active"> </div>}"-->

day4 2018-3-22
<h3>自定义404页面：</h3>

注意在app 的 __init__ 文件里定义错误处理的路由：方式如下：

 <!-- {( 

  @app.errorhandler(404)
  def page_not_found(error):
      return render_template('404.html')
    
    )} -->
    
<h3>后台管理页面搭建：</h3>

flask 蓝图flask.Blueprint 蓝图可以使app各模块分离，使程序结构更加清晰 容易维护

蓝图定义：

 admin __init__ 下定义：
 
 admin = Blueprint('admin', __name__)
 
 在app __init__ 注册 app.register_blueprint(admin, url_prefix="/admin")
 
 注意 url_prefix 参数 将使admin 的访问地址变为 localhost:5000/admin
 
 因此可以使用url_prefix 动态的创建路由
 
 蓝图定以后 路由的定义为@admin.route('/')
 
day4 2018-3-23

完成了网站前后台管理页面的搭建

