<template lang="pug">
tr
  td {{ date }}
  td {{ name }}
  td {{ dice }}
  td {{ result }}
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
