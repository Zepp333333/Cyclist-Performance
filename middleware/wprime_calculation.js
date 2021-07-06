function computeWPrimeBal(streamsByType, activity) {
  let wPrime = activity.icu_w_prime
  let cp = activity.icu_ftp
  if (!wPrime || !cp) return []
  let time = streamsByType.time.data
  let data = streamsByType.watts.data
  if (!time || !data) return null
  if (time.length === 0 || data.length === 0) return []
  data = data.slice()
  let wb = wPrime
  let pt = 0
  for (let i = 0; i < data.length; i++) {
    let t = time[i]
    let secs = t - pt
    let deltaW = cp - data[i]
    if (deltaW > 0) {
      for (let j = 0; j < secs; j++) wb += deltaW * (wPrime - wb) / wPrime
    } else {
      wb += deltaW * secs
    }
    data[i] = Math.floor(wb)
    pt = t
  }
  return data
