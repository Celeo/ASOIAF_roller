<template>
<tr>
  <td>{{ date }}</td>
  <td>{{ name }}</td>
  <td>{{ dice }}</td>
  <td>{{ result }}</td>
</tr>
</template>

<script>
export default {
  props: [
    'date',
    'name',
    'dice',
    'result'
  ],
  data() {
    return {}
  }
}
</script>
