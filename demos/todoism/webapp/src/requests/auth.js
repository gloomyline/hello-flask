import request from '~/requests/index.js'

export function login (payload) {
  return request.request({
    url: '/api/v1/auth/login',
    data: payload,
    method: 'post',
  })
}

export function logout (payload) {
  return request.request({
    url: '/api/v1/auth/logout',
    data
  })
}
