const getDatesArray = (first, last, cropFirst, cropLast) => {
  var dateArray = [];
  const dateFirst = new Date(first);
  const dateLast = new Date(last);
  const dateCropFirst = cropFirst ? new Date(cropFirst) : new Date(first);
  const dateCropLast = cropLast ? new Date(cropLast) : new Date(last);
  dateFirst.setHours(0, 0, 0);
  dateLast.setHours(24, 0, 0);
  dateCropFirst.setHours(0, 0, 0);
  dateCropLast.setHours(24, 0, 0);

  const dateCurrent = new Date(first);
  for (
    let i = 0;
    i < (dateLast.getTime() - dateFirst.getTime()) / (1000 * 3600 * 24);
    i++
  ) {
    if (dateCurrent >= dateCropFirst && dateCurrent <= dateCropLast) {
      dateArray.push(new Date(dateCurrent).toLocaleDateString());
    }
    dateCurrent.setDate(dateCurrent.getDate() + 1);
  }
  return dateArray;
};

const weekdays = dates => {
  return dates.filter(d => {
    const date = new Date(d);
    return ![0, 6].includes(date.getDay());
  });
};

export default {
  getDatesArray,
  weekdays
};
