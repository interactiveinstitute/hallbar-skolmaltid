<template>
  <div class="GraphTypeAbsenceCalendar">
    <h2>Frånvarokalender</h2>
    <q-calendar
      ref="calendar"
      v-model="selectedDate"
      view="month-scheduler"
      :weekdays="[1, 2, 3, 4, 5]"
      :resources="absenceDates"
      locale="sv-se"
      class="schedule"
    >
      <template #scheduler-resource-day="{ timestamp, resource}">
        <div
          v-if="isOccupied(timestamp, resource.absentDays)"
          class="absent"
          :class="{
            'absent-left': isSnakeHead(timestamp, resource.absentDays),
            'absent-right': isSnakeTail(timestamp, resource.absentDays)
          }"
        />
      </template>
    </q-calendar>
  </div>
</template>

<script>
import backendUtils from '../../js/backend-utils';
import QCal from '@quasar/quasar-ui-qcalendar';

export default {
  name: 'GraphTypeAbsenceCalendar',
  components: {},
  props: {
    graph: {
      type: Object,
      default: function () {
        return {};
      }
    } // Feels like overkill, but eslint wants default type that needs to be a function!?
  },
  data: function () {
    return {
      selectedDate: ''
    };
  },
  computed: {
    absence: function () {
      return this.graph.endpointData.values[1];
    },
    absenceDates: function () {
      const students = [];
      this.absence.forEach((s, i) => {
        const label = s.givenName + ' ' + s.familyName;
        const absentDays = this.getDates(s.dateStart, s.dateEnd); // ['2020-10-19', '2020-10-20', '2020-10-26'];
        students.push({ label: label, absentDays: absentDays });
      });

      return students;
    }
  },
  created: function () {
    const today = QCal.parseTimestamp('2020-10-26');
    console.log('today: ', today);
    const relativeDay = QCal.relativeDays(today, QCal.prevDay, 2, [
      1,
      2,
      3,
      4,
      5
    ]);
  },
  methods: {
    endpoints: function (attached) {
      // Required method for all graph types
      return [
        attached[0],
        '?type=SchoolAbsenceReported&q=refSchool==' + attached[0],
        '?type=DietGroup&q=refSchool==' + attached[0]
      ];
    },
    isOccupied (timestamp, occupiedDates) {
      return occupiedDates.includes(timestamp.date);
    },
    isSnakeHead (timestamp, occupiedDates) {
      if (!this.isOccupied(timestamp, occupiedDates)) {
        return false;
      }
      // console.log('ts:', timestamp);
      const relativeDay = QCal.getDate(
        QCal.relativeDays(timestamp, QCal.prevDay, 1, [1, 2, 3, 4, 5])
      );
      // console.log('jumpdate: ', relativeDay);
      return !occupiedDates.includes(relativeDay);
    },
    isSnakeTail (timestamp, occupiedDates) {
      if (!this.isOccupied(timestamp, occupiedDates)) {
        return false;
      }
      const relativeDay = QCal.getDate(
        QCal.relativeDays(timestamp, QCal.nextDay, 2, [1, 2, 3, 4, 5])
      );
      return !occupiedDates.includes(relativeDay);
    },
    getDates: function (start, end) {
      var dateArray = [];
      const dateStart = new Date(start);
      const dateEnd = new Date(end);
      const currentDate = new Date(start);
      for (
        let i = 0;
        i < (dateEnd.getTime() - dateStart.getTime()) / (1000 * 3600 * 24);
        i++
      ) {
        dateArray.push(new Date(currentDate).toLocaleDateString());
        currentDate.setDate(currentDate.getDate() + 1);
      }
      return dateArray;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.absent {
  background-color: rgb(47, 179, 255);
  height: 100%;
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
