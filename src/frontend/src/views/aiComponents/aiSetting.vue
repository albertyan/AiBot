<template>
    <a-space direction="vertical" style="width:100%">
        <a-card :headStyle="{minHeight:'40px',padding:'10px'}" :bodyStyle="{padding:'10px 15px'}" title="选择智能体" class="card-box">
            <p class="tips1">请选择自动回复的智能体</p>
            <div class="card-div">
                <a-select placeholder="请选择智能体" style="width:100%">
                    <a-select-option key="0" value="0">教师</a-select-option>
                </a-select>
            </div>
        </a-card>
        <a-card :headStyle="{minHeight:'40px',padding:'10px'}" :bodyStyle="{padding:'10px 15px'}" title="回复范围" class="card-box">
            <p class="tips1">选择自动回复的聊天场景</p>
            <div class="card-div">
                <a-radio-group name="radioGroup">
                    <a-radio value="1">单聊</a-radio>
                    <a-radio value="2">群聊</a-radio>
                    <a-radio value="3">全部</a-radio>
                </a-radio-group>
            </div>
            <div class="card-div">
                <a-checkbox>群聊被@时才回复</a-checkbox>
            </div>
            <div class="card-div">
                <a-input type="text" placeholder="群聊同事名单，录入后，群聊中同事的消息会自动忽略"></a-input>
                <div class="tips">多个同事名单用双斜杠“//”分隔开，输入后自动保存。</div>
            </div>
        </a-card>
        <a-card :headStyle="{minHeight:'40px',padding:'10px'}" :bodyStyle="{padding:'10px 15px'}" title="自动打招呼" class="card-box">
            <p class="tips1">当检测到对方通过了你的好友申请后，则自动发送话术组内容</p>
            <div class="card-div">
                 <a-switch></a-switch>
            </div>
            <div class="card-div">
                <a-select placeholder="请选择话术组" style="width:100%">
                    <a-select-option key="0" value="0">教师</a-select-option>
                </a-select>
            </div>
        </a-card>
        <a-card :headStyle="{minHeight:'40px',padding:'10px'}" :bodyStyle="{padding:'10px 15px'}" title="关键词配置" class="card-box">
            <template #extra>
                <a-button type="primary" size="small">添加关键词</a-button>
            </template>
            <p class="tips1">触发关键词回复(非必须)</p>
            <div class="card-div">
                  
            </div>
        </a-card>
        <a-card :headStyle="{minHeight:'40px',padding:'10px'}" :bodyStyle="{padding:'10px 15px'}" title="人群标签" class="card-box">
            <p class="tips1">仅针对单聊标签，设置后只回复对应标签的好友聊天</p>
            <div class="card-div">
                   <a-checkbox-group style="width: 100%">
                        <a-row>
                            <a-col :span="8">
                                <a-checkbox value="A">未分组</a-checkbox>
                            </a-col>
                            <a-col :span="8">
                                <a-checkbox value="B">箭冠</a-checkbox>
                            </a-col>
                            <a-col :span="8">
                                <a-checkbox value="C">云南箭冠</a-checkbox>
                            </a-col>
                            <a-col :span="8">
                                <a-checkbox value="D">楼市通</a-checkbox>
                            </a-col>
                            <a-col :span="8">
                                <a-checkbox value="E">中软</a-checkbox>
                            </a-col>
                            <a-col :span="8">
                                <a-checkbox value="F">邻居</a-checkbox>
                            </a-col>
                            <a-col :span="8">
                                <a-checkbox value="G">车领主</a-checkbox>
                            </a-col>
                            <a-col :span="8">
                                <a-checkbox value="H">同事</a-checkbox>
                            </a-col>
                        </a-row>
                    </a-checkbox-group>
            </div>
        </a-card>
        <a-card :headStyle="{minHeight:'40px',padding:'10px'}" :bodyStyle="{padding:'10px 15px'}" title="白名单" class="card-box">
            <p class="tips1">开启后，仅回复白名单中的好友或群聊</p>
            <div class="card-div">
                 <a-switch></a-switch>
            </div>
            <div class="card-div">
                <a-select placeholder="请选择话术组" style="width:100%">
                    <a-select-option key="0" value="0">教师</a-select-option>
                </a-select>
            </div>
        </a-card>
        <a-card :headStyle="{minHeight:'40px',padding:'10px'}" :bodyStyle="{padding:'10px 15px'}" title="回复过滤词" class="card-box">
            <template #extra>
                <a-button type="primary" size="small">添加过滤词</a-button>
            </template>
            <p class="tips1">Coze中包含过滤词(全匹配)的消息将不会回复给用户</p>
            <div class="card-div">
                 
            </div>
        </a-card>
        <a-card :headStyle="{minHeight:'40px',padding:'10px'}" :bodyStyle="{padding:'10px 15px'}" title="上传用户信息" class="card-box">
            <p class="tips1">将用户的昵称等信息传给Coze</p>
            <div class="card-div">
                 <a-switch></a-switch>
            </div>
        </a-card>
        <a-card :headStyle="{minHeight:'40px',padding:'10px'}" :bodyStyle="{padding:'10px 15px'}" title="识别文件" class="card-box">
            <p class="tips1">开启后可以识别消息的文件并上传到Coze</p>
            <div class="card-div">
                 <a-switch></a-switch>
            </div>
        </a-card>
    </a-space>
</template>
<style>
.card-box{
    width:100%;
    background: #f8f8f8;
}
.card-div{
    padding: 10px 0;
}
.tips,.tips1{
    font-size: 12px;
    color: #999;
    margin-top: 10px;
}
.tips1{
    font-size: 14px;
    margin: 0;
}
</style>