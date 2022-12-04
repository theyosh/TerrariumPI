// Attempt to make alternative history navigation..
import { writable } from "svelte/store";

const routeHistory = writable({
  index: 0,
  history: []
});

export function pushRoute(route) {
  routeHistory.update(rh => {
    // remove stale history
    const history = rh.index
      && rh.history.slice(rh.index)
      || rh.history;

    const current = history.length && history[0] || null;

    if (current)
      return {
        ...rh,
        index: 0,
        history: current
          // if current route is same as the new one - simply replace it
          // (prevents building up the history when making for example searches via querystring)
          ? [route, ...history.slice(current.location === route.location && 1 || 0)]
          : [route, ...history]
      };
  })
}

export function popRoute() {
  let newRoute;
  routeHistory.update(rh => {
    const newIndex = rh.index + 1;

    newRoute = newIndex >= rh.history.length
      ? null
      : rh.history[newIndex];

    return {
      ...rh,
      index: newIndex
    };
  })

  return newRoute;
}

export default routeHistory;
