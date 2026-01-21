 <template>
    <a-card title="添加好友配置" style="width: 100%">
      <template #extra>
        <a-space>
            <a-button type="primary" size="small" @click="showModal">导入名单</a-button>
            <a-button type="default" size="small">记录</a-button>
        </a-space>
      </template>
      <a-alert style="margin-bottom: 10px;"  message='名单剩余可添加0人' type="warning" show-icon />
       <a-form
            ref="formRef"
            name="custom-validation"
            :model="formState"
            :rules="rules"
            v-bind="layout"
        >
            <a-form-item has-feedback label="每日添加上限" name="a1">
            <a-input-number v-model:value="formState.a1" :min="1" :max="100000" placeholder="请输入每日添加上限" style="width: 100%"/>
            </a-form-item>
            <a-form-item has-feedback label="添加间隔(分钟)" name="a2">
            <a-input-number v-model:value="formState.a2" :min="1" :max="100000" placeholder="请输入添加间隔(分钟)" style="width: 100%"/>
            </a-form-item>
            <a-form-item has-feedback label="单次添加人数" name="a3">
            <a-input-number v-model:value="formState.a3" :min="1" :max="100000" placeholder="请输入单次添加人数" style="width: 100%"/>
            </a-form-item>
            <a-form-item has-feedback label="验证消息" name="ai">
              <a-textarea v-model:value="formState.token" type="text" placeholder="请输入添加好友时的验证消息"/> 
            </a-form-item>
            
            <a-form-item :wrapper-col="{ span: 24, offset: '100px' }" style="text-align: right;">
                <a-switch checked-children="关闭任务" un-checked-children="开启任务" /> 
            </a-form-item>
        </a-form>  
        
        <!-- 导入弹框 -->
         <a-modal v-model:open="open" title="导入微信号/手机号名单" okText="立即上传" @ok="handleOk" @cancel="resetForm">
            <a-alert style="margin: 10px 0;"  message='将名单录入到表格中，然后导入即可' type="info" show-icon>
                <template #action>
                    <a-button size="small" type="link">复制模板下载地址</a-button>
                </template>
            </a-alert>
            <a-form
                ref="formRef"
                :model="formState"
                :rules="rules"
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
                style="margin-top: 30px;"
            >
                <a-form-item name="upload" extra="仅支持 xlsx、xls、csv 格式文件">
                    <a-upload
                        v-model:fileList="formState.upload"
                        name="logo"
                        action="/upload.do"
                        list-type="picture"
                    >
                        <a-button type="primary">
                        <template #icon><UploadOutlined /></template>
                        选择文件
                        </a-button>
                    </a-upload>
                </a-form-item>
            </a-form>
        </a-modal>   
    </a-card>
</template>
<script setup>
import {
  UploadOutlined
} from '@ant-design/icons-vue';
import { reactive, ref, toRaw } from 'vue';
const open = ref(false);
const layout = {
  labelCol: {
    style: {
        width: '120px',
    }
  },
  wrapperCol: {
    span: 16
  },
};

const formRef = ref();
const formState = reactive({
  a1: '',
  a2: '',
  modes: undefined,
  ai: undefined,
  md: ''
});
 
// 规则校验 
const rules = {
  a1: [
    {
      required: true,
      trigger: 'change',
      message: '请输入总评论条数限制'
    },
  ],
  a2: [
    {
      required: true,
      trigger: 'change',
      message: '请输入单好友评论次数'
    },
  ],
  modes: [
    {
      required: true,
      trigger: 'change',
      message: '请选择互动模式'
    },
  ],
  ai: [
    {
      required: true,
      trigger: 'change',
      message: '请选择智能体'
    },
  ]
};

const showModal = () => {
  open.value = true;
};
const resetForm = () => {
  formRef.value.resetFields();
};
// 提交
const handleOk = e => {
  console.log(e);
  formRef.value
    .validate()
    .then(() => {
        console.log('values', formState, toRaw(formState));
        open.value = false;
    })
    .catch(error => {
        console.log('error', error);
    });
};
 
</script>