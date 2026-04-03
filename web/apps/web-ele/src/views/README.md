# 人员登记模块 - 重构前阅读操作文档

## 1. 模块概述

本模块实现了人员登记功能，包括人员列表展示、添加、编辑、删除和搜索等基本操作。使用 Vue 3 + TypeScript + Element Plus 技术栈开发，是系统中的一个基础功能模块。

## 2. 文件结构

```
person/
└── index.vue       # 主页面文件
```

## 3. 代码结构分析

### 3.1 脚本部分

#### 3.1.1 依赖导入

```typescript
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
```

#### 3.1.2 状态管理

```typescript
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
  gender: 'male',
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
  { label: '男', value: 'male' },
  { label: '女', value: 'female' },
];
```

#### 3.1.3 方法实现

##### 加载人员列表

```typescript
const loadPersonList = async () => {
  loading.value = true;
  try {
    const response = await getPersonListApi({
      page: page.value,
      pageSize: pageSize.value,
      keyword: keyword.value,
    });
    personList.value = response.data.items;
    total.value = response.data.total;
  } catch {
    ElMessage.error('获取人员列表失败');
  } finally {
    loading.value = false;
  }
};
```

##### 搜索功能

```typescript
const handleSearch = () => {
  page.value = 1;
  loadPersonList();
};
```

##### 分页处理

```typescript
const handlePagination = (current: number, size: number) => {
  page.value = current;
  pageSize.value = size;
  loadPersonList();
};
```

##### 打开添加对话框

```typescript
const openAddDialog = () => {
  editingId.value = null;
  dialogTitle.value = '添加人员';
  form.value = {
    name: '',
    gender: 'male',
    phone: '',
    destination: '',
  };
  dialogVisible.value = true;
};
```

##### 打开编辑对话框

```typescript
const openEditDialog = (person: PersonApi.Person) => {
  editingId.value = person.id;
  dialogTitle.value = '编辑人员';
  form.value = { ...person };
  dialogVisible.value = true;
};
```

##### 保存表单

```typescript
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
```

##### 删除人员

```typescript
const handleDelete = async (id: string) => {
  try {
    await deletePersonApi(id);
    ElMessage.success('删除成功');
    loadPersonList();
  } catch {
    ElMessage.error('删除失败');
  }
};
```

##### 生命周期

```typescript
onMounted(() => {
  loadPersonList();
});
```

### 3.2 模板部分

#### 3.2.1 页面布局

```vue
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
      <!-- 表格列定义 -->
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
      <!-- 表单定义 -->
    </ElDialog>
  </div>
</template>
```

#### 3.2.2 表格列定义

```vue
<ElTableColumn prop="id" label="ID" width="80" />
<ElTableColumn prop="name" label="姓名" />
<ElTableColumn prop="gender" label="性别">
  <template #default="scope">
    {{ scope.row.gender === 'male' ? '男' : '女' }}
  </template>
</ElTableColumn>
<ElTableColumn prop="phone" label="手机号" />
<ElTableColumn prop="destination" label="目的地" />
<ElTableColumn prop="createdAt" label="创建时间" width="180" />
<ElTableColumn label="操作" width="150" fixed="right">
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
```

#### 3.2.3 表单定义

```vue
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
```

### 3.3 样式部分

```vue
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
```

## 4. API 模块实现

### 4.1 API 文件结构

```
api/
└── core/
    ├── person.ts     # 人员登记 API 模块
    └── index.ts      # API 导出文件
```

### 4.2 person.ts 实现

```typescript
import { requestClient } from '#/api/request';

export namespace PersonApi {
  /** 人员信息接口 */
  export interface Person {
    id?: string;
    name: string;
    gender: 'female' | 'male';
    phone: string;
    destination: string;
    createdAt?: string;
    updatedAt?: string;
  }

  /** 分页查询参数 */
  export interface PersonQuery {
    page?: number;
    pageSize?: number;
    keyword?: string;
  }

  /** 分页查询结果 */
  export interface PersonListResult {
    items: Person[];
    total: number;
    page: number;
    pageSize: number;
  }
}

/**
 * 获取人员列表
 */
export async function getPersonListApi(params: PersonApi.PersonQuery) {
  return requestClient.get<PersonApi.PersonListResult>('/api/core/person', {
    params,
  });
}

/**
 * 获取人员详情
 */
export async function getPersonDetailApi(id: string) {
  return requestClient.get<PersonApi.Person>(`/api/core/person/${id}`);
}

/**
 * 添加人员
 */
export async function addPersonApi(data: PersonApi.Person) {
  return requestClient.post<PersonApi.Person>('/api/core/person', data);
}

/**
 * 更新人员
 */
export async function updatePersonApi(id: string, data: PersonApi.Person) {
  return requestClient.put<PersonApi.Person>(`/api/core/person/${id}`, data);
}

/**
 * 删除人员
 */
export async function deletePersonApi(id: string) {
  return requestClient.delete(`/api/core/person/${id}`);
}
```

### 4.3 API 导出配置

在 `api/core/index.ts` 文件中添加 person API 的导出：

```typescript
export * from './person';
```

### 4.4 API 调用说明

| API 方法 | 功能 | 参数 | 说明 |
|---------|------|------|------|
| `getPersonListApi` | 获取人员列表 | `{ page, pageSize, keyword }` | 支持分页和搜索 |
| `getPersonDetailApi` | 获取人员详情 | `id` | 获取单个人员信息 |
| `addPersonApi` | 添加人员 | `{ name, gender, phone, destination }` | 创建新人员 |
| `updatePersonApi` | 更新人员 | `id, { name, gender, phone, destination }` | 更新现有人员 |
| `deletePersonApi` | 删除人员 | `id` | 删除指定人员 |

## 5. 功能说明

### 5.1 核心功能

1. **人员列表展示**：显示所有人员信息，包括ID、姓名、性别、手机号、目的地和创建时间
2. **添加人员**：通过对话框表单添加新人员
3. **编辑人员**：通过对话框表单编辑现有人员信息
4. **删除人员**：删除指定人员
5. **搜索功能**：根据关键词搜索人员
6. **分页功能**：支持分页浏览人员列表

### 5.2 数据流程

1. 页面加载时，调用 `loadPersonList` 方法获取人员列表
2. 用户可以通过搜索框输入关键词，点击搜索按钮或按回车键触发搜索
3. 用户可以点击分页控件切换页码或调整每页显示数量
4. 用户点击"添加人员"按钮，打开添加对话框
5. 用户点击"编辑"按钮，打开编辑对话框，显示当前人员信息
6. 用户在对话框中填写表单，点击"保存"按钮提交数据
7. 用户点击"删除"按钮，删除指定人员

## 6. 界面元素

### 6.1 主要组件

1. **页面标题**：显示"人员登记"标题
2. **添加按钮**：点击打开添加对话框
3. **搜索栏**：包含输入框和搜索按钮
4. **表格**：显示人员列表，包含操作按钮
5. **分页控件**：用于分页导航
6. **对话框**：用于添加和编辑人员信息
7. **表单**：包含姓名、性别、手机号和目的地字段

### 6.2 交互流程

1. **查看人员列表**：页面加载后自动显示人员列表
2. **搜索人员**：输入关键词，点击搜索按钮或按回车键
3. **添加人员**：点击"添加人员"按钮，填写表单，点击"保存"按钮
4. **编辑人员**：点击表格中的"编辑"按钮，修改表单，点击"保存"按钮
5. **删除人员**：点击表格中的"删除"按钮，确认后删除
6. **分页操作**：点击分页控件的页码或调整每页显示数量

## 7. 代码优化建议

1. **模块化拆分**：将表单逻辑拆分为单独的组件，提高代码可维护性
2. **使用组合式API**：进一步利用Vue 3的组合式API，将相关逻辑组织在一起
3. **类型定义优化**：完善TypeScript类型定义，提高代码类型安全性
4. **表单验证**：添加表单验证逻辑，确保数据合法性
5. **错误处理**：增强错误处理机制，提供更友好的错误提示
6. **批量操作**：添加批量删除功能，提高操作效率
7. **状态管理**：考虑使用Pinia进行状态管理，特别是在复杂场景下
8. **代码风格**：统一代码风格，遵循项目的代码规范
9. **性能优化**：添加虚拟滚动等性能优化措施，提高大数据量下的渲染性能
10. **可扩展性**：设计更具可扩展性的架构，便于后续功能扩展

## 8. 技术栈

- **前端框架**：Vue 3
- **开发语言**：TypeScript
- **UI 组件库**：Element Plus
- **状态管理**：Vue 3 Composition API (ref)
- **网络请求**：Axios (封装)
- **构建工具**：Vite

## 9. 总结

本模块实现了一个基本的人员登记功能，包含了人员的增删改查操作。代码结构清晰，功能完整，但存在一些可优化的空间。通过模块化拆分、类型优化、表单验证等措施，可以进一步提高代码的可维护性和用户体验。

在后续的重构中，可以考虑使用项目中已有的通用组件和工具，如`useZqTable`、`Form`组件等，以保持代码风格的一致性，并提高开发效率。
