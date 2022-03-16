import { formatDistanceToNow } from "date-fns";
import fr from "date-fns/locale/fr/index.js";

export const capitalize = (text: string) =>
  text.charAt(0).toUpperCase() + text.slice(1);

export const formatToNow = (date: Date) =>
  formatDistanceToNow(date, { addSuffix: true, locale: fr });
