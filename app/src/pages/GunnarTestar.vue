<template>
  <q-page padding>
    <h1>Frånvaro</h1>
    <!-- <q-btn label="next" @click="calendarNext()" /> -->
    <q-calendar
      ref="calendar"
      v-model="selectedDate"
      view="month-scheduler"
      :weekdays="[1, 2, 3, 4, 5]"
      :resources="highlightedStudents"
      locale="sv-se"
    >
      <template #scheduler-resource-day="{ timestamp, resource}">
        <div v-if="isOccupied(timestamp, resource.absentDays)" class="absent" :class="{'absent-left': isSnakeHead(timestamp, resource.absentDays), 'absent-right': isSnakeTail(timestamp, resource.absentDays) }">
          <!-- head: {{ isSnakeHead(timestamp, resource.absentDays) }}
          tail: {{ isSnakeTail(timestamp, resource.absentDays) }}
          {{ resource.absentDays.includes(timestamp.date) }} -->
          <!-- {{ resource.label }} -->
        </div>
      </template>
    </q-calendar>
  </q-page>
</template>

<script>
import QCal from '@quasar/quasar-ui-qcalendar';
export default {
  name: 'GunnarTestar',
  data () {
    return {
      selectedDate: '',
      highlightedStudents: [
        {
          label: 'Gunnar',
          absentDays: [
            '2020-10-26',
            '2020-10-27',
            '2020-10-29',
            '2020-10-31'
          ]
        },
        {
          label: 'Lisa',
          absentDays: [
            '2020-10-26',
            '2020-10-27',
            '2020-10-28'
          ]
        },
        {
          label: 'Eva',
          absentDays: [
            '2020-10-21',
            '2020-10-22',
            '2020-10-23'
          ]
        },
        {
          label: 'Oskar',
          absentDays: [
            '2020-10-19',
            '2020-10-20',
            '2020-10-26'
          ]
        },
        {
          label: 'Ronja',
          absentDays: [
            '2020-10-09',
            '2020-10-26',
            '2020-10-27',
            '2020-10-29'
          ]
        }
      ]
    };
  },
  created () {
    const today = QCal.parseTimestamp('2020-10-26');
    console.log('today: ', today);
    const relativeDay = QCal.relativeDays(today, QCal.prevDay, 2, [1, 2, 3, 4, 5]);
    console.log(QCal.getDate(relativeDay));
  },
  methods: {
    isOccupied (timestamp, occupiedDates) {
      return occupiedDates.includes(timestamp.date);
    },
    isSnakeHead (timestamp, occupiedDates) {
      if (!this.isOccupied(timestamp, occupiedDates)) {
        return false;
      }
      // console.log('ts:', timestamp);
      const relativeDay = QCal.getDate(QCal.relativeDays(timestamp, QCal.prevDay, 1, [1, 2, 3, 4, 5]));
      // console.log('jumpdate: ', relativeDay);
      return !occupiedDates.includes(relativeDay);
    },
    isSnakeTail (timestamp, occupiedDates) {
      if (!this.isOccupied(timestamp, occupiedDates)) {
        return false;
      }
      console.log('ts:', timestamp.date);
      const relativeDay = QCal.getDate(QCal.relativeDays(timestamp, QCal.nextDay, 2, [1, 2, 3, 4, 5]));
      console.log('jumpdate: ', relativeDay);
      return !occupiedDates.includes(relativeDay);
    }
  }
};
</script>

<style scoped>
.absent {
  background-color: rgb(47, 179, 255);
  height: 80%;
  overflow: hidden;
  width: calc(100% + 0.2rem);
}

.absent-left {
  border-top-left-radius: 1rem;
  border-bottom-left-radius: 1rem;
}

.absent-right {
  border-top-right-radius: 1rem;
  border-bottom-right-radius: 1rem;
}

</style>
