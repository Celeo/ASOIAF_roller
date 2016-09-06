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
  props: ['entry'],
  data() {
    return {
      date: '',
      name: '',
      dice: '',
      result: ''
    }
  },
  created: function() {
    this.date = this.entry.date
    this.name = this.entry.name
    this.dice = this.entry.dice
    this.result = this.entry.result
  }
}
</script>
