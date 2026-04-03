<script setup lang="ts">
import type { PersonApi } from '#/api/core/person';

import { onMounted, ref } from 'vue';

import { Delete, Edit, Plus, Search } from '@element-plus/icons-vue';
import {
  ElButton,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElInput as ElInputComp,
  ElMessage,
  ElOption,
  ElPagination,
  ElSelect,
  ElTable,
  ElTableColumn,
} from 'element-plus';

import {
  addPersonApi,
  deletePersonApi,
  getPersonListApi,
  updatePersonApi,
} from '#/api/core/person';

// 表格数据
const personList = ref<PersonApi.Person[]>([]);
const total = ref(0);
const page = ref(1);
const pageSize = ref(10);
const keyword = ref('');

// 对话框状态
const dialogVisible = ref(false);
const dialogTitle = ref('添加人员');

// 表单数据
const form = ref<PersonApi.Person>({
  name: '',
  gender: '0',
  phone: '',
  destination: '',
});

// 加载状态
const loading = ref(false);
const formLoading = ref(false);

// 编辑模式
const editingId = ref<null | string>(null);

// 性别选项
const genderOptions = [
  { label: '男', value: '0' },
  { label: '女', value: '1' },
];

// 加载人员列表
const loadPersonList = async () => {
  loading.value = true;
  try {
    const response = await getPersonListApi({
      page: page.value,
      pageSize: pageSize.value,
      keyword: keyword.value,
    });
    personList.value = response.items;
    total.value = response.total;
  } catch {
    ElMessage.error('获取人员列表失败');
  } finally {
    loading.value = false;
  }
};

// 搜索
const handleSearch = () => {
  page.value = 1;
  loadPersonList();
};

// 分页
const handlePagination = (current: number, size: number) => {
  page.value = current;
  pageSize.value = size;
  loadPersonList();
};

// 打开添加对话框
const openAddDialog = () => {
  editingId.value = null;
  dialogTitle.value = '添加人员';
  form.value = {
    name: '',
    gender: '0',
    phone: '13768893456',
    destination: '',
  };
  dialogVisible.value = true;
};

// 打开编辑对话框
const openEditDialog = (person: PersonApi.Person) => {
  editingId.value = person.id;
  dialogTitle.value = '编辑人员';
  form.value = { ...person };
  dialogVisible.value = true;
};

// 保存
const handleSave = async () => {
  formLoading.value = true;
  try {
    if (editingId.value) {
      // 编辑
      await updatePersonApi(editingId.value, form.value);
      ElMessage.success('更新成功');
    } else {
      // 添加
      await addPersonApi(form.value);
      ElMessage.success('添加成功');
    }
    dialogVisible.value = false;
    loadPersonList();
  } catch {
    ElMessage.error('操作失败');
  } finally {
    formLoading.value = false;
  }
};

// 删除
const handleDelete = async (id: string) => {
  try {
    await deletePersonApi(id);
    ElMessage.success('删除成功');
    loadPersonList();
  } catch {
    ElMessage.error('删除失败');
  }
};

// 生命周期
onMounted(() => {
  loadPersonList();
});
</script>

<template>
  <div class="person-page">
    <div class="page-header">
      <h2>人员登记</h2>
      <ElButton type="primary" @click="openAddDialog" :icon="Plus">
        添加人员1
      </ElButton>
    </div>

    <div class="search-bar">
      <ElInput
        v-model="keyword"
        placeholder="请输入姓名或手机号"
        style="width: 300px"
        :prefix-icon="Search"
        @keyup.enter="handleSearch"
      />
      <ElButton type="primary" @click="handleSearch"> 搜索 </ElButton>
    </div>

    <ElTable v-loading="loading" :data="personList" style="width: 100%" border>
      <ElTableColumn prop="id" label="ID" width="280" />
      <ElTableColumn prop="name" label="姓名" />
      <ElTableColumn prop="gender" label="性别">
        <template #default="scope">
          {{ scope.row.gender === '0' ? '男' : '女' }}
        </template>
      </ElTableColumn>
      <ElTableColumn prop="phone" label="手机号" />
      <ElTableColumn prop="destination" label="目的地" />
      <ElTableColumn prop="sys_create_datetime" label="创建时间" width="180" />
      <ElTableColumn label="操作" width="250" fixed="right">
        <template #default="scope">
          <ElButton
            type="primary"
            size="small"
            @click="openEditDialog(scope.row)"
            :icon="Edit"
          >
            编辑
          </ElButton>
          <ElButton
            type="danger"
            size="small"
            @click="handleDelete(scope.row.id!)"
            :icon="Delete"
          >
            删除
          </ElButton>
        </template>
      </ElTableColumn>
    </ElTable>

    <div class="pagination">
      <ElPagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handlePagination"
        @current-change="handlePagination"
      />
    </div>

    <!-- 表单对话框 -->
    <ElDialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <ElForm :model="form" label-width="80px">
        <ElFormItem label="姓名" prop="name" required>
          <ElInputComp v-model="form.name" placeholder="请输入姓名" />
        </ElFormItem>
        <ElFormItem label="性别" prop="gender" required>
          <ElSelect v-model="form.gender" placeholder="请选择性别">
            <ElOption
              v-for="option in genderOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </ElSelect>
        </ElFormItem>
        <ElFormItem label="手机号" prop="phone" required>
          <ElInputComp v-model="form.phone" placeholder="请输入手机号" />
        </ElFormItem>
        <ElFormItem label="目的地" prop="destination" required>
          <ElInputComp v-model="form.destination" placeholder="请输入目的地" />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <span class="dialog-footer">
          <ElButton @click="dialogVisible = false">取消</ElButton>
          <ElButton type="primary" @click="handleSave" :loading="formLoading">
            保存
          </ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<style scoped>
.person-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
