import { requestClient } from '#/api/request';

export namespace PersonApi {
  /** 人员信息接口 */
  export interface Person {
    id?: string;
    name: string;
    gender: '0' | '1';
    phone: string;
    destination: string;
    sys_create_datetime?: string;
    sys_update_datetime?: string;
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
