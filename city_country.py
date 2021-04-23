def format_city_country(city, country, population=''):
    """Return neatly formatted City, Country format for a city and a country."""
    if population:
        formatted_city_country = str(city).title() + ', ' \
                                 + str(country).title() + '- population ' \
                                 + str(population)
    else:
        formatted_city_country = str(city).title() + ', ' + str(country).title()
    return formatted_city_country
