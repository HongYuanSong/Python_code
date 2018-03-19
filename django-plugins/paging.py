__author__ = 'shy'
__date__ = '2018/3/19 18:23'


class Pagination(object):
    """
    基于Bootstrap样式的数据分页
    """
    def __init__(self, data_count, current_page_num, per_page_data_num=10, max_page_num=7):
        """
        分页参数初始化
        :param data_count: 数据个数
        :param current_page_num: 当前页码
        :param per_page_data_num: 每页数据个数
        :param max_page_num: 最大分页个数
        """
        try:
            current_page_num = int(current_page_num)
            if current_page_num <= 0:
                current_page_num = 1
            self.current_page_num = current_page_num
        except Exception as e:
            self.current_page_num = 1

        self.data_count = data_count
        self.per_page_data_num = per_page_data_num
        self.max_page_num = max_page_num

    @property
    def first_page_num(self):
        """起始页码数"""
        return (self.current_page_num - 1) * self.per_page_data_num

    @property
    def last_page_num(self):
        """终止页码数"""
        if (self.data_count - self.per_page_data_num * self.current_page_num) <= self.per_page_data_num:
            return self.data_count
        return self.current_page_num * self.per_page_data_num

    @property
    def total_page_unm(self):
        """总页码数"""
        integer, decimal = divmod(self.data_count, self.per_page_data_num)
        if decimal == 0:
            return integer
        return integer + 1

    @property
    def page_num_range(self):
        """显示页码范围"""
        if self.total_page_unm < self.max_page_num:
            return range(1, self.total_page_unm + 1)
        part = int(self.max_page_num / 2)
        if self.current_page_num <= part:
            return range(1, self.max_page_num + 1)
        elif (self.current_page_num + part) > self.total_page_unm:
            return range(self.total_page_unm - self.max_page_num + 1, self.total_page_unm + 1)
        else:
            return range(self.current_page_num - part, self.current_page_num + part + 1)

    def page_str(self):
        """生成Bootstrap样式分页html字符串"""
        page_res_list = []
        page_url = "paging_test"
        page_tag_style_list = ["pagination", "pagination pagination-sm", "pagination pagination-lg"]

        ul_tag_start = "<ul class='{0}'>".format(page_tag_style_list[0])
        page_res_list.append(ul_tag_start)

        if self.current_page_num != 1:
            first_tag = "<li><a href='paging_test?p=1'>首页</a></li>"
            page_res_list.append(first_tag)
            prev_tag = "<li><a href='{0}?p={1}'>上一页</a></li>".format(page_url, self.current_page_num - 1)
            page_res_list.append(prev_tag)
        for i in self.page_num_range:
            if i == self.current_page_num:
                temp = "<li class='active'><a href='{0}?p={1}'>{2}</a></li>".format(page_url, i, i)
            else:
                temp = "<li><a href='{0}?p={1}'>{2}</a></li>".format(page_url, i, i)
            page_res_list.append(temp)

        if self.current_page_num != self.total_page_unm:
            next_tag = "<li><a href='{0}?p={1}'>下一页</a></li>".format(page_url, self.current_page_num + 1)
            page_res_list.append(next_tag)
            last_tag = "<li><a href='{0}?p={1}'>尾页</a></li>".format(page_url, self.total_page_unm)
            page_res_list.append(last_tag)

        ul_tag_end = "</ul>"
        page_res_list.append(ul_tag_end)
        page_res_str = ''.join(page_res_list)

        return page_res_str
