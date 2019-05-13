#! /bin/bash
: '
Usage:

    USER=root PASSWORD=root ./deploy.sh 192.168.x.1,192.168.x.2
'
# auto gen by hoobit-core
PROJECT_NAME='GRAPE-TCMS'


INSTALL_PATH="/data/${PROJECT_NAME}"
CURRENT_COMMITID=`git rev-parse --verify HEAD`
ORIGIN=`git remote -v | grep origin | awk '{print $2}' | head -n 1`

CURRENT_BRANCH=`git rev-parse --abbrev-ref HEAD`
if [[ ${CURRENT_BRANCH} == "HEAD" ]]; then  # checkout by commit-id
    CURRENT_BRANCH=`git branch --contains ${CURRENT_COMMITID} | tail -n 1`
fi
if [[ ${CURRENT_BRANCH} =~ ^\*.* ]]; then
    # default release branch is master, for fix github Checking out {commit_id} as master
    CURRENT_BRANCH="master"
fi


function echoo {
    echo -e "\033[32m$@\033[0m"
}


function mssh() {
    sshpass -p ${PASSWORD} ssh -o StrictHostKeyChecking=no ${USER}@${host} $1
}


function deploy() {
    for host in $(echo $1 | tr "," "\n")
    do
        echoo "deploy to ${host} ..."

        isGitRepo=`mssh "[ -d ${INSTALL_PATH} ] && \
            cd ${INSTALL_PATH} && \
            git rev-parse --is-inside-work-tree" || echo $?`

        if [[ "${isGitRepo}" != "true" ]]; then
            echoo "not a git repo, first deploy ..."
            mssh "sudo rm -rf ${INSTALL_PATH} && \
                cd /data && \
                git clone ${ORIGIN} ${INSTALL_PATH}"
        fi

        REMOTE_BRANCH=`mssh "cd ${INSTALL_PATH} && git branch | grep \* | cut -d ' ' -f2"`
        if [[ ${REMOTE_BRANCH} != ${CURRENT_BRANCH} ]]; then
            mssh "cd ${INSTALL_PATH} && \
                git fetch -f origin ${CURRENT_BRANCH}:${CURRENT_BRANCH}"
        else
            mssh "cd ${INSTALL_PATH} && \
                git pull origin ${CURRENT_BRANCH}"
        fi

        mssh "cd ${INSTALL_PATH} && \
            git checkout ${CURRENT_BRANCH} && git checkout ${CURRENT_COMMITID}"

        REMOTE_COMMITID=`mssh "cd ${INSTALL_PATH} && git rev-parse --verify HEAD"`
        echoo "remote ${REMOTE_COMMITID}"

        if [[ ${REMOTE_COMMITID} != ${CURRENT_COMMITID} ]]; then
            echoo "deploy failed, please check. Maybe need push curent branch to origin."
            exit 1
        fi

        mssh "cd ${INSTALL_PATH} && docker-compose down && docker-compose up -d"
    done
}


echoo "deploy...\n\tbranch: ${CURRENT_BRANCH}\n\tcommitid: ${CURRENT_COMMITID}\n\torigin: ${ORIGIN}"

deploy $1