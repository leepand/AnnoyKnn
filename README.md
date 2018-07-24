#### 场景说明

模型用于广告素材信息的抽取和推荐

#### 使用逻辑

- text_summarize_predict 用于长文本文本信息的抽取，训练输入：文本内容-标题对(pair)，比如用户在微博、微信上发表的信息，预测输出：给定长文本，生成标题信息（用于与素材图片信息的关联，图像抽取的信息为短文本）
- img_info_extract_train 用于素材图片特征-短文本的关联训练，原理：提取对象检测模型的倒数第二层激活/隐层状态特征（4096维）作为新模型的输入，原检测模型的最后一层分类（标签1XN-N为分类数）通过word2vec转换成dense embedding，并连接到原检测模型的最后一层（1X300），重新训练，输出：给定短文本的mean-embedding，返回近似素材，该输出为视频推荐（比如在优酷上推荐广告，给定优酷的标题+用户微博等信息预测的标题，返回相关素材）时使用，再将该topN的素材信息的倒数第二层embedding联合素材标题/text_summarize_predict以及其他用户、广告信息计算ctr，并返回最终的最优排序
- 逻辑图：

![resource](/Users/leepand/Downloads/BigRLab_APIs/demoday_fs/nlp/Seq2Seq_Tutorial/github_info_recom/image_text_info_extract/resource.jpg)