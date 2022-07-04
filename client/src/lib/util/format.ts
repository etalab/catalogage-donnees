import * as datefns from "date-fns";
import { fr } from "date-fns/locale";

export const pluralize = (
  amount: number,
  singleText: string,
  pluralText: string
): string => {
  if (amount === 1) {
    return singleText;
  }
  return pluralText;
};

export const capitalize = (text: string): string => {
  return text.charAt(0).toUpperCase() + text.slice(1);
};

export const formatHTMLDate = (date: Date): string => {
  return datefns.format(date, "yyyy-MM-dd");
};

export const formatFullDate = (date: Date): string => {
  return datefns.format(date, "d LLLL yyyy", { locale: fr });
};

export const formatDaysMonthsOrYearsToNow = (date: Date): string => {
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

export const splitParagraphs = (text: string): string[] => {
  return text.split("\n");
};

export const slugify = (str: string): string => {
  str = str.replace(/^\s+|\s+$/g, "");

  // Make the string lowercase
  str = str.toLowerCase();

  // Remove accents, swap ñ for n, etc
  const from =
    "ÁÄÂÀÃÅČÇĆĎÉĚËÈÊẼĔȆÍÌÎÏŇÑÓÖÒÔÕØŘŔŠŤÚŮÜÙÛÝŸŽáäâàãåčçćďéěëèêẽĕȇíìîïňñóöòôõøðřŕšťúůüùûýÿžþÞĐđßÆa·/_,:;".split(
      ""
    );
  const to =
    "AAAAAACCCDEEEEEEEEIIIINNOOOOOORRSTUUUUUYYZaaaaaacccdeeeeeeeeiiiinnooooooorrstuuuuuyyzbBDdBAa------".split(
      ""
    );
  from.forEach((_, index) => {
    str = str.replace(new RegExp(from[index], "g"), to[index]);
  });

  str = str
    .replace(/[^a-z0-9 -]/g, "")
    // Collapse whitespace and replace by -
    .replace(/\s+/g, "-")
    // Collapse dashes
    .replace(/-+/g, "-");

  return str;
};
