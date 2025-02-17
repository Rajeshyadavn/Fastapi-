pipeline {
  agent any
  stages {
    stage('Build our website') {
      steps {
        sh "$PWD/scripts/build.sh"
      }
    }

    stage('Run unit tests') {
      steps {
        sh "$PWD/scripts/unit_tests.sh"
      }
    }

    stage('Deloy website') {
      steps {
        sh "$PWD/scripts/deploy_website.sh"
      }
    }
  }
}
