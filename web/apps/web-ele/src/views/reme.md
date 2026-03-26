



# ZQ Platform 系统页面添加指南

## 1. 项目概述

ZQ Platform 是一个基于 Vue 3 + TypeScript + Element Plus 的企业级管理系统，采用模块化设计，支持快速开发和扩展。本文档详细介绍如何在系统中添加新的功能页面，以人员登记页面为例，提供完整的实现流程。

## 2. 页面添加流程

### 2.1 目录结构

在 `src/views/_core/` 目录下创建新的页面目录，例如 `person/`，包含以下文件：

```
person/
├── index.vue          # 主页面
├── data.ts            # 数据配置
└── modules/
    └── form.vue       # 编辑表单组件
```

### 2.2 API 模块实现

在 `src/api/core/` 目录下创建 `person.ts` 文件：

```typescript
import { requestClient } from '#/api/request';

export namespace PersonApi {
  /** 人员信息接口 */
  export interface Person {
    id?: string;
    name: string;
    gender: 'male' | 'female';
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
    name?: string;
    phone?: string;
    destination?: string;
  }

  /** 分页查询结果 */
  export interface PersonListResult {
    items: Person[];
    total: number;
    page: number;
    pageSize: number;
  }

  /** 批量删除参数 */
  export interface BatchDeleteParams {
    ids: string[];
  }
}

/**
 * 获取人员列表
 */
export async function getPersonListApi(params: PersonApi.PersonQuery) {
  return requestClient.get<PersonApi.PersonListResult>('/api/core/person', { params });
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

/**
 * 批量删除人员
 */
export async function batchDeletePersonApi(params: PersonApi.BatchDeleteParams) {
  return requestClient.post('/api/core/person/batch-delete', params);
}
```

### 2.3 数据配置实现

创建 `data.ts` 文件，配置表格列和表单字段：

```typescript
import type { Column } from 'element-plus';
import type { VbenFormSchema } from '#/adapter/form';
import { $t } from '@vben/locales';
import { z } from '#/adapter/form';

/**
 * 获取性别选项
 */
export function getGenderOptions() {
  return [
    { type: 'primary', label: '男', value: 'male' },
    { type: 'info', label: '女', value: 'female' },
  ];
}

/**
 * 获取搜索表单的字段配置
 */
export function useSearchFormSchema(): VbenFormSchema[] {
  return [
    {
      component: 'Input',
      fieldName: 'name',
      label: '姓名',
    },
    {
      component: 'Input',
      fieldName: 'phone',
      label: '手机号',
    },
    {
      component: 'Input',
      fieldName: 'destination',
      label: '目的地',
    },
  ];
}

/**
 * 获取编辑表单的字段配置
 */
export function getFormSchema(): VbenFormSchema[] {
  return [
    {
      component: 'Input',
      fieldName: 'name',
      label: '姓名',
      rules: z
        .string()
        .min(1, '姓名不能为空')
        .max(50, '姓名长度不能超过50个字符'),
    },
    {
      component: 'RadioGroup',
      componentProps: {
        buttonStyle: 'solid',
        options: getGenderOptions(),
        isButton: true,
      },
      defaultValue: 'male',
      fieldName: 'gender',
      label: '性别',
    },
    {
      component: 'Input',
      fieldName: 'phone',
      label: '手机号',
      rules: z
        .string()
        .regex(/^1[3-9]\d{9}$/, '手机号格式错误')
        .min(11, '手机号长度为11位')
        .max(11, '手机号长度为11位'),
    },
    {
      component: 'Input',
      fieldName: 'destination',
      label: '目的地',
      rules: z
        .string()
        .min(1, '目的地不能为空')
        .max(100, '目的地长度不能超过100个字符'),
    },
  ];
}

/**
 * 获取 ZqTable 表格列配置
 */
export function useZqTableColumns(): Column[] {
  return [
    {
      key: 'name',
      dataKey: 'name',
      title: '姓名',
      width: 120,
    },
    {
      key: 'gender',
      title: '性别',
      width: 80,
      align: 'center' as const,
      slots: { default: 'cell-gender' },
    },
    {
      key: 'phone',
      dataKey: 'phone',
      title: '手机号',
      width: 130,
    },
    {
      key: 'destination',
      dataKey: 'destination',
      title: '目的地',
      width: 150,
    },
    {
      key: 'createdAt',
      dataKey: 'createdAt',
      title: '创建时间',
      width: 180,
    },
    {
      key: 'actions',
      title: '操作',
      width: 150,
      fixed: true,
      align: 'center' as const,
      slots: { default: 'cell-actions' },
    },
  ];
}
```

### 2.4 编辑表单组件实现

创建 `modules/form.vue` 文件：

```vue
<script setup lang="ts">
import type { PersonApi } from '#/api/core/person';
import { ref, watch } from 'vue';
import { ElDialog, ElMessage, ElNotification } from 'element-plus';
import { Form } from '@vben/common-ui';
import { $t } from '@vben/locales';
import { addPersonApi, updatePersonApi } from '#/api/core/person';
import { getFormSchema } from '../data';

interface Props {
  visible?: boolean;
  model?: PersonApi.Person;
}

const props = withDefaults(defineProps<Props>(), {
  visible: false,
  model: () => ({}),
});

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void;
  (e: 'success'): void;
}>();

const formRef = ref<InstanceType<typeof Form>>();
const formValues = ref<PersonApi.Person>({} as PersonApi.Person);
const loading = ref(false);
const dialogTitle = ref('添加人员');

// 监听 model 变化
watch(
  () => props.model,
  (newVal) => {
    if (newVal) {
      formValues.value = { ...newVal };
      dialogTitle.value = '编辑人员';
    } else {
      formValues.value = {} as PersonApi.Person;
      dialogTitle.value = '添加人员';
    }
  },
  { immediate: true, deep: true },
);

// 监听 visible 变化
watch(
  () => props.visible,
  (newVal) => {
    if (newVal && formRef.value) {
      formRef.value?.reset();
    }
  },
);

// 打开对话框
function open(model?: PersonApi.Person) {
  if (model) {
    formValues.value = { ...model };
    dialogTitle.value = '编辑人员';
  } else {
    formValues.value = {} as PersonApi.Person;
    dialogTitle.value = '添加人员';
  }
  emit('update:visible', true);
}

// 关闭对话框
function close() {
  emit('update:visible', false);
}

// 提交表单
async function handleSubmit() {
  if (!formRef.value) return;

  const valid = await formRef.value.validate();
  if (!valid) return;

  loading.value = true;
  try {
    if (formValues.value.id) {
      // 更新
      await updatePersonApi(formValues.value.id, formValues.value);
      ElNotification.success({
        title: '成功',
        message: '更新人员成功',
      });
    } else {
      // 添加
      await addPersonApi(formValues.value);
      ElNotification.success({
        title: '成功',
        message: '添加人员成功',
      });
    }
    emit('success');
    close();
  } catch (error: any) {
    ElMessage.error(error?.message || '操作失败');
  } finally {
    loading.value = false;
  }
}

defineExpose({
  open,
});
</script>

<template>
  <ElDialog
    v-model="props.visible"
    :title="dialogTitle"
    width="500px"
    @close="close"
  >
    <Form
      ref="formRef"
      v-model="formValues"
      :schema="getFormSchema()"
      :loading="loading"
      @submit="handleSubmit"
    />
  </ElDialog>
</template>
```

### 2.5 主页面实现

创建 `index.vue` 文件：

```vue
<script setup lang="ts">
import type { PersonApi } from '#/api/core/person';
import { ref } from 'vue';
import { Page } from '@vben/common-ui';
import { Edit, Plus, Trash2 } from '@vben/icons';
import { $t } from '@vben/locales';
import { ElButton, ElMessage, ElMessageBox, ElTag } from 'element-plus';
import { batchDeletePersonApi, deletePersonApi, getPersonListApi } from '#/api/core/person';
import { useZqTable } from '#/components/zq-table';
import { getGenderOptions, useSearchFormSchema, useZqTableColumns } from './data';
import Form from './modules/form.vue';

defineOptions({ name: 'SystemPerson' });

const formRef = ref<InstanceType<typeof Form>>();
const selectedRows = ref<PersonApi.Person[]>([]);

// 状态映射
const genderOptions = getGenderOptions();

type TagType = 'danger' | 'info' | 'primary' | 'success' | 'warning';

function getTagType(value: any, options: any[]): TagType {
  const option = options.find((o) => o.value === value);
  return (option?.type as TagType) || 'info';
}

function getTagLabel(value: any, options: any[]): string {
  const option = options.find((o) => o.value === value);
  return option?.label || String(value);
}

/**
 * 编辑人员
 */
function onEdit(row: PersonApi.Person) {
  formRef.value?.open(row);
}

/**
 * 创建新人员
 */
function onCreate() {
  formRef.value?.open();
}

/**
 * 删除单个人员
 */
function onDelete(row: PersonApi.Person) {
  ElMessageBox.confirm(
    `确定要删除人员「${row.name}」吗？`,
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    },
  )
    .then(async () => {
      try {
        await deletePersonApi(row.id!);
        ElMessage.success(`删除人员「${row.name}」成功`);
        refreshGrid();
      } catch {
        ElMessage.error('删除失败');
      }
    })
    .catch(() => {
      // 用户取消了操作
    });
}

/**
 * 批量删除人员
 */
function onBatchDelete() {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要删除的人员');
    return;
  }

  // 确认删除
  const names = selectedRows.value.map((row: PersonApi.Person) => row.name).join('、');
  const confirmMessage = `确定要删除选中的 ${selectedRows.value.length} 个人员吗？\n${names}`;

  ElMessageBox.confirm(confirmMessage, '批量删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(async () => {
      try {
        // 批量删除
        const ids = selectedRows.value.map((row: PersonApi.Person) => row.id!);
        await batchDeletePersonApi({ ids });
        ElMessage.success(`删除成功，共删除 ${selectedRows.value.length} 个人员`);
        selectedRows.value = [];
        refreshGrid();
      } catch {
        ElMessage.error('删除失败');
      }
    })
    .catch(() => {
      // 用户取消了操作
    });
}

// 处理选择变化
function handleSelectionChange(items: Record<string, any>[]) {
  selectedRows.value = items as PersonApi.Person[];
}

// 列表 API
const fetchPersonList = async (params: any) => {
  const res = await getPersonListApi({
    page: params.page.currentPage,
    pageSize: params.page.pageSize,
    keyword: params.form?.name || params.form?.phone || params.form?.destination,
  });
  return {
    items: res.data.items,
    total: res.data.total,
  };
};

// 使用 ZqTable
const [Grid, gridApi] = useZqTable({
  gridOptions: {
    columns: useZqTableColumns(),
    border: true,
    stripe: true,
    showSelection: true,
    showIndex: true,
    proxyConfig: {
      autoLoad: true,
      ajax: {
        query: fetchPersonList,
      },
    },
    pagerConfig: {
      enabled: true,
      pageSize: 20,
    },
    toolbarConfig: {
      search: true,
      refresh: true,
      zoom: true,
      custom: true,
    },
  },
  formOptions: {
    schema: useSearchFormSchema(),
    showCollapseButton: false,
    submitOnChange: false,
  },
});

/**
 * 刷新表格
 */
function refreshGrid() {
  gridApi.reload();
}
</script>

<template>
  <Page auto-content-height>
    <Form ref="formRef" @success="refreshGrid" />

    <Grid @selection-change="handleSelectionChange">
      <!-- 工具栏操作 -->
      <template #toolbar-actions>
        <ElButton type="primary" :icon="Plus" @click="onCreate">
          添加人员
        </ElButton>
        <ElButton type="danger" plain @click="onBatchDelete">
          批量删除
          {{ selectedRows.length > 0 ? `(${selectedRows.length})` : '' }}
        </ElButton>
      </template>

      <!-- 性别列 -->
      <template #cell-gender="{ row }">
        <ElTag :type="getTagType(row.gender, genderOptions)" size="small">
          {{ getTagLabel(row.gender, genderOptions) }}
        </ElTag>
      </template>

      <!-- 操作列 -->
      <template #cell-actions="{ row }">
        <ElButton link type="primary" :icon="Edit" @click="onEdit(row)">
          编辑
        </ElButton>
        <ElButton
          link
          type="danger"
          :icon="Trash2"
          @click="onDelete(row)"
        >
          删除
        </ElButton>
      </template>
    </Grid>
  </Page>
</template>
```

### 2.6 菜单配置

1. **登录系统**：使用管理员账号登录
2. **进入菜单管理**：导航到 "系统管理" -> "菜单管理"
3. **添加菜单**：
  - 点击 "新增" 按钮
  - 填写菜单信息：
    - 菜单名称：人员登记
    - 路由路径：/system/person
    - 组件路径：/views/_core/person/index.vue
    - 图标：ic:round-people
    - 父级菜单：系统管理
  - 保存菜单配置

## 3. 后端接口实现

需要后端实现以下 API 接口：

| 接口路径 | 方法 | 功能 |
|---------|------|------|
| `/api/core/person` | GET | 获取人员列表（支持分页和搜索） |
| `/api/core/person/:id` | GET | 获取人员详情 |
| `/api/core/person` | POST | 添加人员 |
| `/api/core/person/:id` | PUT | 更新人员 |
| `/api/core/person/:id` | DELETE | 删除人员 |
| `/api/core/person/batch-delete` | POST | 批量删除人员 |

## 4. 最佳实践

1. **遵循项目结构**：按照现有的目录结构和命名规范组织代码
2. **使用 TypeScript**：确保类型安全，提高代码可维护性
3. **复用组件**：使用项目提供的通用组件，如 `useZqTable`、`Form` 等
4. **统一错误处理**：使用 ElMessage 和 ElNotification 提供一致的用户反馈
5. **模块化设计**：将代码拆分为多个模块，提高可维护性
6. **遵循 API 规范**：按照项目现有的 API 设计模式实现接口
7. **添加适当的注释**：提高代码可读性
8. **测试功能**：确保所有功能正常工作

## 5. 常见问题

1. **菜单不显示**：
  - 检查菜单配置是否正确
  - 确保用户有相应的权限
  - 检查路由配置是否正确

2. **API 调用失败**：
  - 检查后端接口是否实现
  - 检查 API URL 是否正确
  - 检查网络连接是否正常

3. **表单验证失败**：
  - 检查表单字段规则是否正确
  - 确保必填字段已填写
  - 检查数据格式是否符合要求

4. **批量操作失败**：
  - 确保后端支持批量操作接口
  - 检查选中的数据是否正确

## 6. 技术栈

- **前端框架**：Vue 3 + TypeScript
- **UI 组件**：Element Plus
- **状态管理**：Pinia
- **路由**：Vue Router
- **网络请求**：Axios (封装)
- **构建工具**：Vite
- **后端框架**：FastAPI
- **数据库**：PostgreSQL

## 7. 总结

通过以上步骤，您可以在 ZQ Platform 系统中添加新的功能页面。遵循项目的设计模式和最佳实践，可以确保代码的一致性和可维护性。

添加新页面的核心步骤包括：
1. 创建 API 模块，定义数据类型和接口
2. 创建页面目录结构，包括主页面和组件
3. 实现数据配置，包括表格列和表单字段
4. 实现编辑表单组件，处理数据提交
5. 实现主页面，展示数据和操作
6. 通过菜单管理添加菜单配置
7. 确保后端实现相应的 API 接口

按照这些步骤，您可以快速、规范地添加新的功能页面，保持系统的一致性和可扩展性。
        
