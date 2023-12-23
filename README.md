# RPC service using a microservices architecture
This project originates from the 2023 Computer Network curse from UnB (Universidade de Brasília). It's divided in four
different projects: an RPC Client, a Proxy Server and two servers to compute the requests. This project is dedicated to
the proxy server.
## Motivation
Containers are a technology similar to virtualization (VMWare, VirtualBox, QEMU, Hyper-V), but only
the User part is virtualized, allowing the same system to behave like a range of systems,
using your own package manager, dependency versions, environment settings and everything else.
This technology has increasingly grown in popularity, as it allows reproducibility of environments and
prevent applications from interfering with each other, something common in non-isolated environments, exposing only the
ports referring to services offered to the external network.
## Motivation
Each student must create a docker-compose.yml file that defines multiple complementary services
or interdependent with each other, as they would do in a commercial application. The file, containing at least 4
services, must be submitted together with a report explaining the reason for choosing the services, how they were
configured to interconnect your services, and how it can be used in a real situation (e.g. business).
The link to a video presentation with the student using the services must also be provided
hosted in the containers.
