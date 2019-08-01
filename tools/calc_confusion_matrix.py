#!/usr/python
#coding=utf-8

#二项式分布计算可信度
#
import pandas as pd

class TPD(object):

    '''
    TPD 数据预测效果查看函数
    '''
    def __init__(self):
        #print("预测数据需要包含如下两列：")
        #print("sampleID,Predict（需要pandas数据框格式！！！）")
        #cohort	sampleID	type	bi_type
        self.__DATA__ = '''DL	56	A	B
DL	54	A	B
DL	53	A	B
DL	52	A	B
DL	50	A	B
DL	47	A	B
DL	46	A	B
DL	38	A	B
DL	36	A	B
DL	34	A	B
DL	32	A	B
DL	31	A	B
DL	30	A	B
DL	28	A	B
DL	27	A	B
DL	23	A	B
DL	22	A	B
DL	20	A	B
DL	18	A	B
DL	16	A	B
DL	15	A	B
DL	14	A	B
DL	13	A	B
DL	12	A	B
DL	11	A	B
DL	10	A	B
DL	2	A	B
DL	1	A	B
DL	55	C	M
DL	51	C	M
DL	49	C	M
DL	48	C	M
DL	45	C	M
DL	43	C	M
DL	42	C	M
DL	41	C	M
DL	40	C	M
DL	39	C	M
DL	37	C	M
DL	35	C	M
DL	33	C	M
DL	29	C	M
DL	26	C	M
DL	24	C	M
DL	21	C	M
DL	19	C	M
DL	17	C	M
DL	9	C	M
DL	8	C	M
DL	7	C	M
DL	6	C	M
DL	5	C	M
DL	4	C	M
DL	86	M	B
DL	72	M	B
DL	96	N	B
DL	93	N	B
DL	92	N	B
DL	91	N	B
DL	88	N	B
DL	85	N	B
DL	79	N	B
DL	77	N	B
DL	76	N	B
DL	75	N	B
DL	71	N	B
DL	69	N	B
DL	68	N	B
DL	67	N	B
DL	66	N	B
DL	65	N	B
DL	59	N	B
DL	97	P	M
DL	95	P	M
DL	94	P	M
DL	90	P	M
DL	89	P	M
DL	87	P	M
DL	84	P	M
DL	83	P	M
DL	82	P	M
DL	81	P	M
DL	80	P	M
DL	78	P	M
DL	74	P	M
DL	73	P	M
DL	70	P	M
DL	64	P	M
DL	63	P	M
DL	62	P	M
DL	61	P	M
DL	60	P	M
DL	58	P	M
DL	57	P	M
ZY	12301_repA	A	B
ZY	123010_repA	A	B
ZY	123011_repA	A	B
ZY	123012_repA	A	B
ZY	123013_repA	A	B
ZY	123014_repA	A	B
ZY	123015_repA	A	B
ZY	123016_repA	A	B
ZY	123017_repA	A	B
ZY	123018_repA	A	B
ZY	123019_repA	A	B
ZY	12302_repA	A	B
ZY	12303_repA	A	B
ZY	12304_repA	A	B
ZY	12305_repA	A	B
ZY	12306_repA	A	B
ZY	12307_repA	A	B
ZY	12308_repA	A	B
ZY	12309_repA	A	B
ZY	12311_repA	P	M
ZY	123110_repA	P	M
ZY	123111_repA	P	M
ZY	123112_repA	P	M
ZY	123113_repA	P	M
ZY	123114_repA	P	M
ZY	123115_repA	P	M
ZY	123116_repA	P	M
ZY	123117_repA	P	M
ZY	123118_repA	P	M
ZY	123119_repA	P	M
ZY	12312_repA	P	M
ZY	123120_repA	P	M
ZY	12313_repA	P	M
ZY	12314_repA	P	M
ZY	12315_repA	P	M
ZY	12316_repA	P	M
ZY	12317_repA	P	M
ZY	12318_repA	P	M
ZY	12319_repA	P	M
ZY	12321_repA	C	M
ZY	123210_repA	C	M
ZY	123211_repA	C	M
ZY	123212_repA	C	M
ZY	123213_repA	C	M
ZY	123214_repA	C	M
ZY	123215_repA	C	M
ZY	12322_repA	C	M
ZY	12323_repA	C	M
ZY	12324_repA	C	M
ZY	12325_repA	C	M
ZY	12326_repA	C	M
ZY	12327_repA	C	M
ZY	12328_repA	C	M
ZY	12329_repA	C	M
ZE	25831	A	B
ZE	25832	A	B
ZE	25833	A	B
ZE	25834	A	B
ZE	25835	A	B
ZE	25836	A	B
ZE	25837	A	B
ZE	25839	A	B
ZE	25841	M	B
ZE	25843	M	B
ZE	25844	M	B
ZE	25845	M	B
ZE	25846	M	B
ZE	25847	M	B
ZE	25848	M	B
ZE	25849	M	B
ZE	25851	C	M
ZE	25852	C	M
ZE	25853	C	M
ZE	25854	C	M
ZE	25855	C	M
ZE	25856	C	M
ZE	25857	C	M
ZE	25858	C	M
ZE	25861	P	M
ZE	25862	P	M
ZE	25863	P	M
ZE	25864	P	M
ZE	25865	P	M
ZE	25866	P	M
ZE	25867	P	M
ZE	25868	P	M
ZE	25869	P	M
ZE	258310	A	B
ZE	258311	A	B
ZE	258312	A	B
ZE	258315	A	B
ZE	258316	A	B
ZE	258318	A	B
ZE	258321	A	B
ZE	258322	A	B
ZE	258323	A	B
ZE	258326	A	B
ZE	258327	A	B
ZE	258328	A	B
ZE	258330	A	B
ZE	258332	A	B
ZE	258333	A	B
ZE	258334	A	B
ZE	258336	A	B
ZE	258337	A	B
ZE	258338	A	B
ZE	258339	A	B
ZE	258340	A	B
ZE	258341	A	B
ZE	258342	A	B
ZE	258343	A	B
ZE	258346	A	B
ZE	258348	A	B
ZE	258350	A	B
ZE	258410	M	B
ZE	258411	M	B
ZE	258412	M	B
ZE	258413	M	B
ZE	258414	M	B
ZE	258415	M	B
ZE	258416	M	B
ZE	258417	M	B
ZE	258420	M	B
ZE	258421	M	B
ZE	258422	M	B
ZE	258423	M	B
ZE	258424	M	B
ZE	258425	M	B
ZE	258426	M	B
ZE	258427	M	B
ZE	258428	M	B
ZE	258429	M	B
ZE	258430	M	B
ZE	258432	M	B
ZE	258433	M	B
ZE	258435	M	B
ZE	258436	M	B
ZE	258438	M	B
ZE	258439	M	B
ZE	258440	M	B
ZE	258441	M	B
ZE	258442	M	B
ZE	258443	M	B
ZE	258444	M	B
ZE	258445	M	B
ZE	258446	M	B
ZE	258448	M	B
ZE	258449	M	B
ZE	258450	M	B
ZE	258510	C	M
ZE	258511	C	M
ZE	258512	C	M
ZE	258513	C	M
ZE	258610	P	M
ZE	258611	P	M
ZE	258612	P	M
ZE	258613	P	M
ZE	258614	P	M
ZE	258615	P	M
ZE	258616	P	M
ZE	258617	P	M
ZE	258618	P	M
ZE	258619	P	M
ZE	258620	P	M
ZE	258621	P	M
ZE	258622	P	M
ZE	258623	P	M
ZE	258624	P	M
ZE	258625	P	M
ZE	258626	P	M
ZE	258627	P	M
ZE	258628	P	M
ZE	258629	P	M
ZE	258630	P	M
ZE	258631	P	M
ZE	258632	P	M
ZE	258633	P	M
ZE	258634	P	M
ZE	258636	P	M
ZE	258637	P	M
ZE	258638	P	M
ZE	258639	P	M
ZE	258640	P	M
ZE	258641	P	M
ZE	258642	P	M
ZE	258643	P	M
ZE	258644	P	M
ZE	258645	P	M
ZE	258646	P	M
ZE	258647	P	M
ZE	258648	P	M
ZE	258649	P	M
ZE	258650	P	M'''
        self.data = []
        self.predict = []

    # 初始化
    def init(self):
        self.data = [line.split("\t") for line in self.__DATA__.split("\n")]
        self.data = pd.DataFrame(self.data, columns=["cohort", "sampleID", "type", "bi_type"])
        #self.data["predict"] = []

    # 设置预测数据
    def set(self, predict, type=4):
        pass

    # 查找某一个ID
    def find(self, id):
        pass

    # 合并表格
    def merge_matrix(self, predict_data, type=3):

        predict_data.columns = ['ID', 'pType']
        if type not in [2,3]:
            print("type 必须在3和4选择！")
            exit(0)
        result = pd.concat([self.data, predict_data], join='inner', axis=1)
        TF = []
        for indexs in result.index:
            if(result.loc[indexs].values[type] == result.loc[indexs].values[5]):
                TF.append(1)
            else:
                TF.append(0)
        # 合并表单
        result["TF"] = TF
        return result[["cohort", "pType", "TF"]]


    # 计算混淆矩阵
    def calc_confusion_matrix(self, predict_data):
        data = self.merge_matrix(predict_data, 3)
        corhot = set(data["cohort"])
        ptype = set(data["pType"])

        tag = {}
        for hot in corhot:
            tag[hot] = {}
            for tp in ptype:
                tag[hot][tp] = {}
                tag[hot][tp]['T'] = len(data[(data["cohort"] == hot) & (data["pType"] == tp) & (data["TF"] == 1)])
                tag[hot][tp]['F'] = len(data[(data["cohort"] == hot) & (data["pType"] == tp) & (data["TF"] == 0)])
        return tag

    # 计算多分类混淆矩阵
    def calc_confusion_matrix_more(self, predict_data):
        data = self.merge_matrix(predict_data, 2)
        corhot = set(data["cohort"])
        ptype = set(data["pType"])

        tag = {}
        for hot in corhot:
            tag[hot] = {}
            for tp in ptype:
                tag[hot][tp] = {}
                tag[hot][tp]['T'] = len(data[(data["cohort"] == hot) & (data["pType"] == tp) & (data["TF"] == 1)])
                tag[hot][tp]['F'] = len(data[(data["cohort"] == hot) & (data["pType"] == tp) & (data["TF"] == 0)])
        return tag


    # 计算ACC
    def calc_acc(self, predict_data):
        pass


if __name__ == "__main__":
    pass

