export class Dataset {
  constructor ({name = null, description = null, coverUrl = null} = {}) {
    this.name = name
    this.description = description
    this.coverUrl = coverUrl
  }
}

export function createDataset (data) {
  const name = data.name
  const description = data.description
  const coverUrl = data.coverUrl
  return Object.freeze(new Dataset(name, description, coverUrl))
}
