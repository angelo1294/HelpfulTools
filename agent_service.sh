wget https://jenkins-itest.spirenteng.com/jenkins/view/qa_itest/job/itest_Installer_nightly/lastSuccessfulBuild/artifact/artifacts/velocity-agent-linux.gtk.x86_64.run
chmod +x velocity-agent-linux.gtk.x86_64.run
./velocity-agent-linux.gtk.x86_64.run
sed -i "s/.*COMMAND=\/usr\/bin\/python2.7*/COMMAND=\/usr\/bin\/python3/" /opt/spirent/velocity-agent/configuration/script.interpreters.ini
sed -i 's/.*SCRIPT_INTERPRETER_SETTINGS*/SCRIPT_INTERPRETER_SETTINGS=\/opt\/spirent\/velocity-agent\/configuration\/script.interpreters.ini/' /etc/opt/spirent/velocity-agent/agent.conf
velo="$(hostname)"
sed -i 's/.*VELOCITY_HOST*/VELOCITY_HOST=${velo}/' /etc/opt/spirent/velocity-agent/agent.conf
rm velocity-agent-linux.gtk.x86_64.run
service velocity-agent start