<template>
  <div>
    <div mb-3>
      <TheInput
        mb-3
        v-model="username"
        placeholder="What's your username?"
        autocomplete="false"
      />
    </div>
    <div mb-4>
      <TheInput
        v-model="password"
        placeholder="What's your password?"
        autocomplete="false"
      />
    </div>
    <div>
      <button
        class="m-3 text-sm btn"
        :disabled="!username || !password"
        @click="login"
      >
        Login
      </button>
    </div>
  </div>
</template>

<script setup lang="ts" generic="T extends any, O extends any">
import { login as _login } from '~/requests/auth';

const username = ref<string>('');
const password = ref<string>('');

async function  login () {
  const response = await _login({ username: unref(username), password: unref(password) });
  console.log(111, response);
}
</script>