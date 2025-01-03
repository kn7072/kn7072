import request_1
#from urllib import urlencode
import json


class Client(object):
    def __init__(self, url):
        """
        Initialises a new Client object


        :param url: This is where the BrowserMob Proxy lives
        """
        self.host = "http://" + url
        resp = request_1.post('%s/proxy' % self.host, {})  #  urlencode('')
        jcontent = json.loads(resp.content)
        self.port = jcontent['port']
        url_parts = self.host.split(":")
        self.proxy = url_parts[1][2:] + ":" + str(self.port)

    def close(self):
        """
        shuts down the proxy and closes the port
        """
        r = request_1.delete('%s/proxy/%s' % (self.host, self.port))
        return r.status_code

    # webdriver integration
    # ...as a proxy object
    def selenium_proxy(self):
        """
        Returns a Selenium WebDriver Proxy class with details of the HTTP Proxy
        """
        from selenium import webdriver
        return webdriver.Proxy({
            "httpProxy": self.proxy,
            "sslProxy": self.proxy,
        })

    def webdriver_proxy(self):
        """
        Returns a Selenium WebDriver Proxy class with details of the HTTP Proxy
        """
        return self.selenium_proxy()

    # ...as a capability
    def add_to_capabilities(self, capabilities):
        """
        Adds an 'proxy' entry to a desired capabilities dictionary with the
        BrowserMob proxy information


        :param capabilities: The Desired capabilities object from Selenium WebDriver
        """
        capabilities['proxy'] = {'proxyType': "MANUAL",
                                 'httpProxy': self.proxy}

    def add_to_webdriver_capabilities(self, capabilities):
        self.add_to_capabilities(capabilities)

    # browsermob proxy api
    @property
    def har(self):
        """
        Gets the HAR that has been recorded
        """
        r = request_1.get('%s/proxy/%s/har' % (self.host, self.port))

        return r.json()

    def new_har(self, ref=None, options={}):
        """
        This sets a new HAR to be recorded


        :param ref: A reference for the HAR. Defaults to None
        :param options: A dictionary that will be passed to BrowserMob Proxy \
                   with specific keywords. Keywords are: \
                   captureHeaders - Boolean, capture headers \
                   captureContent - Boolean, capture content bodies \
                   captureBinaryContent - Boolean, capture binary content
        """
        if ref:
            payload = {"initialPageRef": ref}
        else:
            payload = {}
        if options:
            payload.update(options)

        r = request_1.put('%s/proxy/%s/har' % (self.host, self.port), payload)
        if r.status_code == 200:
            return (r.status_code, r.json())
        else:
            return (r.status_code, None)

    def new_page(self, ref=None):
        """
        This sets a new page to be recorded


        :param ref: A reference for the new page. Defaults to None
        """
        if ref:
            payload = {"pageRef": ref}
        else:
            payload = {}
        r = request_1.put('%s/proxy/%s/har/pageRef' % (self.host, self.port),
                         payload)
        return r.status_code

    def blacklist(self, regexp, status_code):
        """
        Sets a list of URL patterns to blacklist


        :param regex: a comma separated list of regular expressions
        :param status_code: the HTTP status code to return for URLs that do not \
                       match the blacklist

        """
        r = request_1.put('%s/proxy/%s/blacklist' % (self.host, self.port),
                         {'regex': regexp, 'status': status_code})
        return r.status_code

    def whitelist(self, regexp, status_code):
        """
        Sets a list of URL patterns to whitelist


        :param regex: a comma separated list of regular expressions
        :param status_code: the HTTP status code to return for URLs that do not \
                       match the whitelist
        """
        r = request_1.put('%s/proxy/%s/whitelist' % (self.host, self.port),
                         {'regex': regexp, 'status': status_code})
        return r.status_code

    def basic_authentication(self, domain, username, password):
        """
        This add automatic basic authentication


        :param domain: domain to set authentication credentials for
        :param username: valid username to use when authenticating
        :param  password: valid password to use when authenticating
        """
        r = request_1.post(url='%s/proxy/%s/auth/basic/%s' % (self.host, self.port, domain),
                          data=json.dumps({'username': username, 'password': password}),
                          headers={'content-type': 'application/json'})
        return r.status_code

    def headers(self, headers):
        """
        This sets the headers that will set by the proxy on all requests


        :param headers: this is a dictionary of the headers to be set
        """
        if not isinstance(headers, dict):
            raise TypeError("headers needs to be dictionary")

        r = request_1.post(url='%s/proxy/%s/headers' % (self.host, self.port),
                          data=json.dumps(headers),
                          headers={'content-type': 'application/json'})
        return r.status_code

    def response_interceptor(self, js):
        """
        Executes the javascript against each response


        :param js: the javascript to execute
        """
        r = request_1.post(url='%s/proxy/%s/interceptor/response' % (self.host, self.port),
                  data=js,
                  headers={'content-type': 'x-www-form-urlencoded'})
        return r.status_code

    def request_interceptor(self, js):
        """
        Executes the javascript against each request


        :param js: the javascript to execute
        """
        r = request_1.post(url='%s/proxy/%s/interceptor/request' % (self.host, self.port),
                  data=js,
                  headers={'content-type': 'x-www-form-urlencoded'})
        return r.status_code

    LIMITS = {
        'upstream_kbps': 'upstreamKbps',
        'downstream_kbps': 'downstreamKbps',
        'latency': 'latency'
    }

    def limits(self, options):
        """
        Limit the bandwidth through the proxy.


        :param options: A dictionary with all the details you want to set. \
                        downstreamKbps - Sets the downstream kbps \
                        upstreamKbps - Sets the upstream kbps \
                        latency - Add the given latency to each HTTP request
        """
        params = {}

        for (k, v) in options.items():
            if k not in self.LIMITS:
                raise KeyError('invalid key: %s' % k)

            params[self.LIMITS[k]] = int(v)

        if len(params.items()) == 0:
            raise KeyError("You need to specify one of the valid Keys")

        r = request_1.put('%s/proxy/%s/limit' % (self.host, self.port),
                         params)
        return r.status_code

    TIMEOUTS = {
        'request': 'requestTimeout',
        'read': 'readTimeout',
        'connection': 'connectionTimeout',
        'dns': 'dnsCacheTimeout'
    }

    def timeouts(self, options):
        """
        Configure various timeouts in the proxy


        :param options: A dictionary with all the details you want to set. \
                        request - request timeout (in seconds) \
                        read - read timeout (in seconds) \
                        connection - connection timeout (in seconds) \
                        dns - dns lookup timeout (in seconds)
        """
        params = {}

        for (k, v) in options.items():
            if k not in self.TIMEOUTS:
                raise KeyError('invalid key: %s' % k)

            params[self.TIMEOUTS[k]] = int(v)

        if len(params.items()) == 0:
            raise KeyError("You need to specify one of the valid Keys")

        r = request_1.put('%s/proxy/%s/timeout' % (self.host, self.port),
                         params)
        return r.status_code

    def remap_hosts(self, address, ip_address):
        """
        Remap the hosts for a specific URL


        :param address: url that you wish to remap
        :param ip_address: IP Address that will handle all traffic for the address passed in
        """
        assert address is not None and ip_address is not None
        r = request_1.post('%s/proxy/%s/hosts' % (self.host, self.port),
                         json.dumps({address: ip_address}),
                          headers={'content-type': 'application/json'})
        return r.status_code

    def wait_for_traffic_to_stop(self, quiet_period, timeout):
        """
        Waits for the network to be quiet


        :param quiet_period: number of miliseconds the network needs to be quiet for
        :param timeout: max number of miliseconds to wait
        """
        r = request_1.put('%s/proxy/%s/wait' % (self.host, self.port),
                 {'quietPeriodInMs': quiet_period, 'timeoutInMs': timeout})
        return r.status_code

    def clear_dns_cache(self):
        """
        Clears the DNS cache associated with the proxy instance
        """
        r = request_1.delete('%s/proxy/%s/dns/cache' % (self.host, self.port))
        return r.status_code

    def rewrite_url(self, match, replace):
        """
        Rewrites the requested url.


        :param match: a regex to match requests with
        :param replace: unicode \
                   a string to replace the matches with
        """
        params = {
            "matchRegex": match,
            "replace": replace
        }
        r = request_1.put('%s/proxy/%s/rewrite' % (self.host, self.port),
                         params)
        return r.status_code

    def retry(self, retry_count):
        """
        Retries. No idea what its used for, but its in the API...


        :param retry_count: the number of retries
        """
        r = request_1.put('%s/proxy/%s/retry' % (self.host, self.port),
                 {'retrycount': retry_count})
        return r.status_code
