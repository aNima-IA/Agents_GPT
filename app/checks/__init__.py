from .cors import Check as CorsCheck
from .open_redirect import Check as OpenRedirectCheck
from .idor import Check as IDORCheck
from .sensitive_files import Check as SensitiveFilesCheck
from .dir_listing import Check as DirListingCheck
from .ssrf import Check as SSRFCheck
from .jwt_misconfig import Check as JWTCheck
from .csp_weak import Check as CSPCheck
from .graphql_exposure import Check as GraphQLCheck
from .upload_misconfig import Check as UploadCheck
from .verb_tamper import Check as VerbTamperCheck
from .cache_poison import Check as CachePoisonCheck
from .subdomain_takeover import Check as SubdomainCheck
from .auth_weak_headers import Check as AuthWeakCheck
from .rate_limit_missing import Check as RateLimitCheck

ALL_CHECKS = [
    CorsCheck(),
    OpenRedirectCheck(),
    IDORCheck(),
    SensitiveFilesCheck(),
    DirListingCheck(),
    SSRFCheck(),
    JWTCheck(),
    CSPCheck(),
    GraphQLCheck(),
    UploadCheck(),
    VerbTamperCheck(),
    CachePoisonCheck(),
    SubdomainCheck(),
    AuthWeakCheck(),
    RateLimitCheck(),
]
