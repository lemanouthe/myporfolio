<script setup>
defineProps({
  groups: { type: Array, default: () => [] },
});
</script>

<template>
  <div class="manifest">
    <div class="manifest-head">requirements.txt</div>
    <div class="manifest-body">
      <div v-for="group in groups" :key="group.label" class="skill-group">
        <div class="grp-label">{{ group.label }}</div>
        <div v-for="skill in group.skills" :key="skill.name" class="skill-row">
          <span>{{ skill.name }}</span>
          <span class="ver">{{ skill.level_display }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
