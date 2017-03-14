from django.conf import settings

from .defaults import default_headers, default_methods  # Kept here for backwards compatibility


class Settings(object):
    """
    Shadow Django's settings with a little logic
    """

    @property
    def CORS_ALLOW_HEADERS(self):
        return getattr(settings, 'CORS_ALLOW_HEADERS', default_headers)

    @property
    def CORS_ALLOW_METHODS(self):
        return getattr(settings, 'CORS_ALLOW_METHODS', default_methods)

    @property
    def CORS_ALLOW_CREDENTIALS(self):
        return getattr(settings, 'CORS_ALLOW_CREDENTIALS', False)

    @property
    def CORS_PREFLIGHT_MAX_AGE(self):
        return getattr(settings, 'CORS_PREFLIGHT_MAX_AGE', 86400)

    @property
    def CORS_ORIGIN_ALLOW_ALL(self):
        return getattr(settings, 'CORS_ORIGIN_ALLOW_ALL', False)

    @property
    def CORS_ORIGIN_WHITELIST(self):
        import pymysql.cursors

        conf_urls = getattr(settings, 'CORS_ORIGIN_WHITELIST', ())

        db_conf = getattr(settings, 'CORS_ORIGIN_DB_CONF', {})
        if not db_conf:
            return conf_urls

        try:
            db = pymysql.connect(host=db_conf.get("host"),
                                 user=db_conf.get("user"),
                                 password=db_conf.get("password"),
                                 db=db_conf.get("db"),
                                 charset='utf8')

            cursor = db.cursor()
            cursor.execute('select http_url from company')
            results = cursor.fetchall()

            db_urls = [r[0] for r in results]
            white_list = db_urls + conf_urls

        except Exception as e:
            white_list = conf_urls

        finally:
            cursor.close()
            db.commit()
            db.close()
            return white_list

    @property
    def CORS_ORIGIN_REGEX_WHITELIST(self):
        return getattr(settings, 'CORS_ORIGIN_REGEX_WHITELIST', ())

    @property
    def CORS_EXPOSE_HEADERS(self):
        return getattr(settings, 'CORS_EXPOSE_HEADERS', ())

    @property
    def CORS_URLS_REGEX(self):
        return getattr(settings, 'CORS_URLS_REGEX', r'^.*$')

    @property
    def CORS_MODEL(self):
        return getattr(settings, 'CORS_MODEL', None)

    @property
    def CORS_REPLACE_HTTPS_REFERER(self):
        return getattr(settings, 'CORS_REPLACE_HTTPS_REFERER', False)


conf = Settings()
