<template>
  <div>

    <div>
      <div class="border-2  px-10 rounded-xl my-5 w-13 h-10 text-2xl bg-yellow-500 font-black">Unresolved:</div>
      
        <div class="box-border border-4 p-0.5 px-10 mx-auto rounded-2xl bg-yellow-50" v-for="error in unresolved" :key="error.index">`{{ error.code }}` - {{ error.text }}
          
          <button class="box-border border-3 p-0.5 px-10 ml-10 mx-auto rounded-3xl bg-yellow-200"> Resolve </button>
        </div>
      
    </div>
    <div>
      <div class="border-2  px-10 rounded-xl my-5 w-13 h-10 text-2xl bg-green-500 font-black">Resolved:</div>

        <div class="box-border border-4 p-0.5 px-10 mx-auto rounded-2xl bg-green-50" v-for="error in resolved" :key="error.index">`{{ error.code }}` - {{ error.text }}

          <button class="box-border border-3 p-0.5 px-10 ml-10 mx-auto rounded-3xl bg-green-200"> Unresolve </button>

        </div>
    </div>
    <div>
      <div class="border-2  px-10 rounded-xl my-5 w-13 h-10 text-2xl bg-red-500 font-black">Backlog:</div>

        <div class="box-border border-4 p-0.5 px-10 mx-auto rounded-2xl bg-red-50"  v-for="error in backlog" :key="error.index">`{{ error.code }}` - {{ error.text }}

          <button class="box-border border-3 p-0.5 px-10 ml-10 mx-auto rounded-3xl bg-red-200"> Move to Unresolve </button>

        </div>
    </div>
  </div>
</template>

<script>
export default {
  async asyncData({ $axios }) {
    try {
      const { resolved, unresolved, backlog } = await $axios.$get(
        "http://localhost:8000/get_lists"
      );
      return {
        resolved,
        unresolved,
        backlog
      };
    } catch (error) {
      console.log(
        `Couldn't get error lists:\n${error}\nDid you start the API?`
      );
      console.log(
        "HINT: You can comment out the full `asyncData` method and work with mocked data for UI/UX development, if you want to."
      );
    }
  },
  data() {
    return {
      resolved: [],
      unresolved: [],
      backlog: []
    };
  }
};
</script>
