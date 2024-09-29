# à partir d'une moyenne de votes entre 0 et 10, donne la catégorie correspondante (fortement en désaccord, en désaccord, neutre, d'accord, fortement d'accord)
def getCategory(votes):
    average = sum(votes) / len(votes) if len(votes) > 0 else 0
    if average <= 2:
        return 'fortement en désaccord'
    if average <= 4:
        return 'en désaccord'
    if average <= 6:
        return 'neutre'
    if average <= 8:
        return 'd\'accord'
    return 'fortement d\'accord'