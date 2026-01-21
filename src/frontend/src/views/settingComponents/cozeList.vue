<template>
    <a-card title="智能体管理" style="width: 100%">
        <template #extra>
            <a-button type="link" size="small">测试</a-button>
        </template>
        <a-list
            class="demo-loadmore-list"
            :loading="initLoading"
            item-layout="horizontal"
            :data-source="list"
        >
            <template #loadMore>
            <div
                v-if="!initLoading && !loading"
                :style="{ textAlign: 'center', marginTop: '12px', height: '32px', lineHeight: '32px' }"
            >
                <a-button @click="onLoadMore" size="small">更多</a-button>
            </div>
            </template>
            <template #renderItem="{ item }">
            <a-list-item>
                <template #actions>
                    <a class="bg-red-500" key="list-loadmore-del">删除</a>
                </template>
                <a-skeleton :title="false" :loading="!!item.loading" active>
                    <a-list-item-meta
                        description="BOT ID: 24234234234234"
                    >
                        <template #title>
                            <span style="margin-right: 10px;">{{ item.name.last }}</span>
                            <a-tag color="green">默认</a-tag>
                        </template>
                    </a-list-item-meta>
                </a-skeleton>
            </a-list-item>
            </template>
        </a-list>
        <div class="footer">
            <a-button type="primary" @click="showModal">添加智能体</a-button>
        </div>
        <!-- 添加弹框 -->
         <a-modal v-model:open="open" title="添加智能体" @ok="handleOk" @cancel="resetForm">
            <a-form
                ref="formRef"
                :model="formState"
                :rules="rules"
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
                style="margin-top: 30px;"
            >
                <a-form-item ref="name" label="智能体名称" name="name">
                    <a-input v-model:value="formState.name" placeholder="请输入智能体名称"/>
                </a-form-item>
                <a-form-item ref="id" label="BOT ID" name="id">
                    <a-input v-model:value="formState.id" placeholder="请输入BOT ID"/>
                </a-form-item>
                <a-form-item ref="isDefault" label="默认接待" name="isDefault">
                    <a-switch v-model:checked="formState.isDefault" />
                </a-form-item>
            </a-form>
        </a-modal>
    </a-card>
</template>
<script setup>
import { onMounted, reactive, ref, toRaw, nextTick } from 'vue';
const count = 3;
const fakeDataUrl = `https://randomuser.me/api/?results=${count}&inc=name,gender,email,nat,picture&noinfo`;
const initLoading = ref(true);
const loading = ref(false);
const data = ref([]);
const list = ref([]);
onMounted(() => {
  fetch(fakeDataUrl)
    .then(res => res.json())
    .then(res => {
      initLoading.value = false;
      data.value = res.results;
      list.value = res.results;
    });
});
const onLoadMore = () => {
  loading.value = true;
  list.value = data.value.concat(
    [...new Array(count)].map(() => ({
      loading: true,
      name: {},
      picture: {},
    })),
  );
  fetch(fakeDataUrl)
    .then(res => res.json())
    .then(res => {
      const newData = data.value.concat(res.results);
      loading.value = false;
      data.value = newData;
      list.value = newData;
      nextTick(() => {
        // Resetting window's offsetTop so as to display react-virtualized demo underfloor.
        // In real scene, you can using public method of react-virtualized:
        // https://stackoverflow.com/questions/46700726/how-to-use-public-method-updateposition-of-react-virtualized
        window.dispatchEvent(new Event('resize'));
      });
    });
};
// 新增弹框
const open = ref(false);
const formRef = ref();
const labelCol = {
  style:{
      width: '100px'
    }
};
const wrapperCol = {
  span: 16,
};
 
const formState = reactive({
  name: '',
  id: '',
  isDefault: false
});
const rules = {
  name: [
    {
      required: true,
      message: '请输入智能体名称',
      trigger: 'change',
    }
  ],
  id: [
    {
      required: true,
      message: '请输入BOT ID',
      trigger: 'change',
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
<style scoped>
.bg-red-500{
    color: red;
}
.demo-loadmore-list {
  min-height: 100px;
}
.footer{
    text-align: right;
}
</style>