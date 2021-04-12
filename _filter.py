# -*- coding: utf-8 -*-


class Filter(object):
    filter_map = {
        "ArticleType":
            {
                "硕士论文": "4",
                "博士论文": "3",
                "期刊": "1",
            },
        "Subject":
            {
                "生物学": "A006",
                "计算机软件及技术应用": "I138",
                "数学": "A002"
            },
        "Year":

            dict(zip([str(x) for x in range(2002, 2022)], [str(x) for x in range(2002, 2022)])),
        "Order":
            {
                "相关度": "1",
                "发表时间": "2",
                "下载次数": "3",
                "被引次数": "4"
            }

    }

    def __init__(self, **kwargs):
        """
        用于设置过滤文献的参数
        :param kwargs:
        可选参数包括：ArticleType, Subject, Year
        其中，ArticleType的取值为（硕士论文，博士论文，期刊），
        Subject取值暂时支持（生物学，计算机软件及技术应用，数学）
        Year取值为2002-2021，所有参数均为字符串类型
        """
        self.filter = {}
        if kwargs:
            for i in kwargs.keys():
                if i in self.filter_map.keys():
                    self.filter[i] = self.filter_map.get(i).get(kwargs.get(i))
                else:
                    # TODO: 添加其他筛选参数
                    continue

    def get_param(self):
        return self.filter

    def __str__(self):
        return str(self.filter)

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    f = Filter(Subject="生物学", Year='2021', Other="None", ArticleType="硕士论文")
    print(f.get_param())
