import moment from "moment"
import { v1 } from "uuid";

export function getNow() {
  var date = new Date();
  return moment(date).format('DD-MM-YYYY HH:mm:ss')
}

export function getUID() {
  return v1();
}