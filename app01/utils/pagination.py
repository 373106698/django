from django.utils.safestring import mark_safe
import copy

"""
    自定义分页组件

    #1.获取数据库数据

    #2.实例化分页对象
    page_object = Pagination(request,queryset)

    context = {
        "search_data":search_data,

        "queryset":page_object.page_queryset,#分完页的数据
        "page_string":page_object.html() #页码
    }

    return render(request,"number.html",context)


    #3.在html页面中

    {% for obj in queryset %}
        <tr>
            <td>{{obj.id}}</td>
        </tr>
    {% endfor %}

    <ul class="pagination" style="float: left;">
        {{page_string}}
    </ul>

"""

class Pagination(object):

    def __init__(self,request,queryset,page_size=10,page_param="page",plus=5):

        """
        request: 请求的对象
        queryset: 符合条件的数据（根据数据进行分页处理）
        page_size: 每页显示多少条数据
        page_param 在URL中请求获取的分页参数 例如:/list/?page=12
        plus: 显示当页码的前几页后几页
        """

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable =True
        self.query_dict = query_dict


        page = request.GET.get(page_param,"1")

        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        

        self.page = page
        self.page_size = page_size

        #起始页
        self.start = (page-1) * page_size
        self.end = page * page_size

        #分完页的数据
        self.page_queryset = queryset[self.start:self.end]

        #总页码
        total_count = queryset.count()

        total_page_count,div =divmod(total_count,page_size)
        if div:
            total_page_count += 1

        self.total_page_count = total_page_count

        self.plus = plus
        self.page_param = page_param
    
    def html(self):
        #计算出当前页的前5页后5页
        if self.total_page_count <= 2 * self.plus + 1:
            #数据库中的数据较少没有达到11页
            start_page = 1
            end_page = self.total_page_count
        else:
            #数据库中的数据较多时

            #当前页<5
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus +1
            else:
                #当前页>5 总页面
                if (self.page+self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page =self.page - self.plus
                    end_page =self.page + self.plus
        
        #页码
        page_str_list = []

        self.query_dict.setlist(self.page_param,[1])

        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        #上一页

        if self.page > 1:
            self.query_dict.setlist(self.page_param,[self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param,[1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        
        page_str_list.append(prev)

        print(start_page)
        print(end_page)

        #页面
        for i in range(start_page,end_page + 1):
            self.query_dict.setlist(self.page_param,[i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(),i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(),i)
            page_str_list.append(ele)

        #下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param,[self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param,[self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        #尾页
        self.query_dict.setlist(self.page_param,[self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_string ="""
        <li>
            <form style="float: left; margin-left: -1px" method="get">
                <input name="page" 
                    style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;" 
                    type="text" class="form-control" placeholder="页码">
                <button class="btn btn-default" style="border-radius: 0;" type="submit">跳转</button>
            </form>
        </li>
        """
        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))
        return page_string