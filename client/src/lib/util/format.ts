import * as datefns from "date-fns";
import { pluralize } from "../util";

export const capitalize = (text: string) => {
  return text.charAt(0).toUpperCase() + text.slice(1);
};

export const formatDaysMonthsOrYearsToNow = (date: Date) => {
  const now = new Date();

  const daysDiff = datefns.differenceInDays(now, date);
  if (daysDiff < 0) {
    throw new Error(`date should be in the past: ${date}`);
  }
  if (daysDiff === 0) {
    return datefns.isToday(date) ? "aujourd'hui" : "hier";
  }

  const monthsDiff = datefns.differenceInMonths(now, date);
  if (monthsDiff === 0) {
    return daysDiff >= 2 ? `il y a ${daysDiff} jours` : "hier";
  }

  const yearsDiff = datefns.differenceInYears(now, date);
  if (yearsDiff === 0) {
    return `il y a ${monthsDiff} mois`;
  }

  return `il y a ${yearsDiff} an${pluralize(yearsDiff, "", "s")}`;
};
